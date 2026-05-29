import argparse
import csv
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Optional
import xml.etree.ElementTree as ET
import glob
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def parse_res(res_path: Path):
    tree = ET.parse(res_path)
    root = tree.getroot()
    analysis = next(e for e in root.iter() if local_name(e.tag) == "Analysis")
    stepmap = next(e for e in analysis if local_name(e.tag) == "StepMap")

    entities = []
    flat_columns = []
    for entity in [e for e in stepmap if local_name(e.tag) == "Entity"]:
        entity_name = entity.attrib["name"]
        ent_type = entity.attrib.get("entType", "")
        components = []
        for comp in [c for c in entity if local_name(c.tag) == "Component"]:
            comp_name = comp.attrib["name"]
            units = comp.attrib.get("unitsValue", "")
            components.append((comp_name, units))
            flat_columns.append((entity_name, comp_name, units, ent_type))
        entities.append((entity_name, ent_type, components))

    steps = []
    data_nodes = [e for e in analysis if local_name(e.tag) == "Data"]
    for data in data_nodes:
        for step in [s for s in data if local_name(s.tag) == "Step"]:
            if step.attrib.get("type") != "dynamic":
                continue
            raw = step.text or ""
            vals = [float(x) for x in raw.split()]
            steps.append(vals)
    return entities, flat_columns, steps


def write_entity_catalog(path: Path, entities):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["entity_name", "entity_type", "component_name", "units"])
        for entity_name, ent_type, components in entities:
            for comp_name, units in components:
                w.writerow([entity_name, ent_type, comp_name, units])


def load_config(config_path: Optional[Path]):
    if not config_path:
        return {"channels": [], "plots": []}
    return json.loads(config_path.read_text(encoding="utf-8"))


def col_index(flat_columns, entity, component):
    for idx, (entity_name, comp_name, _units, _ent_type) in enumerate(flat_columns):
        if entity_name == entity and comp_name == component:
            return idx
    raise KeyError(f"Missing channel: {entity}.{component}")


def evaluate_channel(channel, flat_columns, steps):
    ctype = channel["type"]
    entity = channel["entity"]
    if ctype == "component":
        comp = channel["component"]
        idx = col_index(flat_columns, entity, comp)
        return [row[idx] for row in steps], channel.get("units", "")
    if ctype == "vector_magnitude":
        comps = channel.get("components", ["FX", "FY", "FZ"])
        idxs = [col_index(flat_columns, entity, comp) for comp in comps]
        return [math.sqrt(sum(row[i] * row[i] for i in idxs)) for row in steps], channel.get("units", "")
    raise ValueError(f"Unsupported channel type: {ctype}")


def detect_launcher(cli_value: Optional[str]):
    candidates = []
    if cli_value:
        candidates.append(cli_value)
    env_launcher = os.environ.get("ADAMS_LAUNCHER")
    if env_launcher:
        candidates.append(env_launcher)

    topdir = os.environ.get("topdir")
    if topdir:
        candidates.append(os.path.join(topdir, "common", "mdi.bat"))

    patterns = [
        r"C:\MSC.Software\Adams\*\common\mdi.bat",
        r"C:\Program Files\MSC.Software\Adams\*\common\mdi.bat",
        r"C:\Hexagon\Adams\*\common\mdi.bat",
        r"C:\Program Files\Hexagon\Adams\*\common\mdi.bat",
    ]
    for pattern in patterns:
        matches = sorted(glob.glob(pattern), reverse=True)
        candidates.extend(matches)

    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(
        "No ADAMS launcher found. Pass --launcher, set ADAMS_LAUNCHER, or run inside an ADAMS-initialized shell."
    )


def make_acf(adm_path: Path, out_prefix: str, end_time: float, steps: int, outdir: Path):
    acf_path = outdir / f"{out_prefix}.acf"
    acf_path.write_text(
        f"{adm_path.name}\n{out_prefix}.out\n\nintegrator/error=1e-4\nSIM/DYN,END={end_time},STEPS={steps}\nSTOP\n",
        encoding="utf-8",
    )
    return acf_path


def make_solver_workspace(prefix: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=f"{prefix}_", dir=tempfile.gettempdir()))


def run_solver(launcher: str, helper_script: Path, acf_path: Path, cwd: Path):
    proc = subprocess.run([launcher, "python", str(helper_script), str(acf_path)], cwd=str(cwd), text=True)
    return proc.returncode


def materialize_helper_script(helper_script: Path) -> Path:
    temp_root = Path(tempfile.gettempdir()) / "adams-batch-analyzer"
    temp_root.mkdir(parents=True, exist_ok=True)
    temp_helper = temp_root / helper_script.name
    shutil.copy2(helper_script, temp_helper)
    return temp_helper


def copy_solver_outputs(workdir: Path, outdir: Path, out_prefix: str):
    copied = []
    for suffix in [".acf", ".out", ".res", ".msg", ".req", ".gra"]:
        src = workdir / f"{out_prefix}{suffix}"
        if src.exists():
            dst = outdir / src.name
            shutil.copy2(src, dst)
            copied.append(dst)
    return copied


def write_selected_channels(path: Path, time_series, evaluated):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s"] + [name for name, _vals in evaluated])
        for idx, t in enumerate(time_series):
            w.writerow([t] + [vals[idx] for _name, vals in evaluated])


def build_plots(outdir: Path, time_series, evaluated_dict, plots):
    created = []
    for plot in plots:
        plt.figure(figsize=(10, 5))
        for series_name in plot["series"]:
            plt.plot(time_series, evaluated_dict[series_name], linewidth=1.6, label=series_name)
        plt.title(plot.get("title", "ADAMS Result Plot"))
        plt.xlabel(plot.get("x_label", "Time (s)"))
        plt.ylabel(plot.get("y_label", "Value"))
        if len(plot["series"]) > 1:
            plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out_path = outdir / plot["output"]
        plt.savefig(out_path, dpi=200)
        plt.close()
        created.append(out_path)
    return created


def write_summary(path: Path, adm_path: Path, out_prefix: str, result_paths, evaluated):
    lines = [
        "# ADAMS Batch Analysis Summary",
        "",
        f"- Model: `{adm_path}`",
        f"- Output prefix: `{out_prefix}`",
        "",
        "## Generated Files",
    ]
    for p in result_paths:
        lines.append(f"- `{p.name}`")
    lines.append("")
    lines.append("## Selected Channels")
    for name, values in evaluated:
        lines.append(f"- `{name}`: min={min(values):.4f}, max={max(values):.4f}, mean={sum(values)/len(values):.4f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run a generic ADAMS batch pipeline.")
    parser.add_argument("--adm", required=True, help="Path to .adm model")
    parser.add_argument("--output-dir", required=True, help="Directory for generated outputs")
    parser.add_argument("--launcher", help="Path to ADAMS launcher batch file")
    parser.add_argument("--end-time", type=float, default=2.7)
    parser.add_argument("--steps", type=int, default=540)
    parser.add_argument("--prefix", help="Output prefix; defaults to <adm stem>_auto")
    parser.add_argument("--config", help="Optional JSON config defining channels and plots")
    args = parser.parse_args()

    adm_path = Path(args.adm).resolve()
    outdir = Path(args.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    out_prefix = args.prefix or f"{adm_path.stem}_auto"
    launcher = detect_launcher(args.launcher)
    helper_script = materialize_helper_script(Path(__file__).with_name("invoke_solver.py"))
    config = load_config(Path(args.config).resolve() if args.config else None)

    solver_workdir = make_solver_workspace(out_prefix)
    work_adm = solver_workdir / adm_path.name
    work_adm.write_text(adm_path.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")

    acf_path = make_acf(work_adm, out_prefix, args.end_time, args.steps, solver_workdir)
    rc = run_solver(launcher, helper_script, acf_path, solver_workdir)
    if rc != 0:
        print(f"Solver failed with code {rc}")
        return rc

    copied_result_paths = copy_solver_outputs(solver_workdir, outdir, out_prefix)
    res_path = outdir / f"{out_prefix}.res"
    msg_path = outdir / f"{out_prefix}.msg"
    entities, flat_columns, steps = parse_res(res_path)
    time_idx = col_index(flat_columns, "time", "TIME")
    time_series = [row[time_idx] for row in steps]

    catalog_path = outdir / f"{out_prefix}_entity_catalog.csv"
    write_entity_catalog(catalog_path, entities)

    evaluated = []
    for channel in config.get("channels", []):
        values, _units = evaluate_channel(channel, flat_columns, steps)
        evaluated.append((channel["name"], values))

    selected_path = outdir / f"{out_prefix}_selected_channels.csv"
    if evaluated:
        write_selected_channels(selected_path, time_series, evaluated)

    evaluated_dict = {name: vals for name, vals in evaluated}
    plot_paths = []
    if config.get("plots") and evaluated_dict:
        plot_paths = build_plots(outdir, time_series, evaluated_dict, config["plots"])

    summary_path = outdir / f"{out_prefix}_summary.md"
    write_summary(
        summary_path,
        adm_path,
        out_prefix,
        [*copied_result_paths, catalog_path, selected_path, *plot_paths],
        evaluated,
    )

    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
