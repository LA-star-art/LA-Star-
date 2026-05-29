# Adams Batch Analyzer

Adams Batch Analyzer is a generic Codex plugin for automating non-interactive ADAMS batch simulation workflows.

Repository:

- https://github.com/LA-star-art/LA-Star-

Chinese documentation:

- [README.zh-CN.md](./README.zh-CN.md)

It is designed for mechanical-system models in general, not only engines. The plugin can:

- run an ADAMS solver job from a `.adm` model
- generate an `.acf` batch control file
- extract `.res` data into CSV
- compute selected scalar or vector-magnitude channels
- generate configurable plots
- write a short markdown summary for each run

## Intended use

Use this plugin when you want to automate solver and post-processing work that would otherwise be repeated manually in ADAMS/PostProcessor.

Typical use cases:

- batch simulation of linkage mechanisms
- repeated suspension or drivetrain studies
- engine firing-force timing studies
- force/torque channel extraction
- plot generation for selected joints, motions, or loads
- reproducible simulation output packaging

## Requirements

- Windows
- ADAMS installed locally
- a valid ADAMS license
- a solver-ready `.adm` model

## Installation notes

This repository is structured as a Codex plugin. Before use, make sure one of the following is true:

1. `ADAMS_LAUNCHER` is set to your ADAMS launcher batch file
2. your shell is already initialized with ADAMS environment variables such as `topdir`
3. ADAMS is installed in a common default location and can be auto-detected

## Main script

```powershell
python scripts\adams_batch_pipeline.py `
  --adm E:\path\to\model.adm `
  --output-dir E:\path\to\outputs `
  --config examples\generic_channels.json
```

Optional arguments:

- `--launcher <path>`: explicit ADAMS launcher path
- `--end-time <float>`: simulation end time
- `--steps <int>`: output steps
- `--prefix <name>`: custom output prefix

## Config format

The pipeline reads a JSON config with two top-level arrays:

- `channels`
- `plots`

`channels` supports:

- `component`
- `vector_magnitude`

See [assets/example_config.json](./assets/example_config.json) for a working example.

The repository also includes:

- [examples/generic_channels.json](./examples/generic_channels.json)
- [examples/engine_channels.json](./examples/engine_channels.json)
- [QUICKSTART.md](./QUICKSTART.md)

## Output files

For each run, the pipeline writes:

- `<prefix>.acf`
- `<prefix>.res`
- `<prefix>.msg`
- `<prefix>_entity_catalog.csv`
- `<prefix>_selected_channels.csv`
- configured plot PNG files
- `<prefix>_summary.md`

## Repository layout

```text
adams-batch-analyzer/
├─ .codex-plugin/
├─ assets/
├─ examples/
├─ scripts/
├─ skills/
├─ LICENSE
├─ README.md
└─ README.zh-CN.md
```

## Development status

Current tested capabilities:

- batch solver invocation
- `.res` parsing
- selected-channel CSV export
- configurable PNG plot generation
- summary markdown export

Validated locally on a Windows machine with ADAMS 2024.1 available.

## Current scope

This plugin focuses on:

- generic batch solver automation
- configurable result extraction
- simple reporting and plotting

It does not currently perform:

- full ADAMS/View GUI editing
- automatic geometry repair
- model-specific semantic interpretation by default

## Open-source preparation status

This version is already structured as a repository-friendly draft for publication under the `LA-star-art/LA-Star-` repository. Before a public release, you may still want to:

- publish example datasets or screenshots
- add CI or packaging steps
- write model-type-specific template configs

## License

This repository is released under the MIT License. See [LICENSE](./LICENSE).

## Contributing

If you plan to continue development or publish improvements, see:

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [OPEN_SOURCE_CHECKLIST.md](./OPEN_SOURCE_CHECKLIST.md)
- [QUICKSTART.md](./QUICKSTART.md)
