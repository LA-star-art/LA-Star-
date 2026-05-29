# Quick Start

## 1. Prerequisites

- Windows
- ADAMS installed locally
- a valid ADAMS license
- a solver-ready `.adm` file

You should also have one of these available:

- `ADAMS_LAUNCHER` environment variable
- an ADAMS-initialized shell with `topdir`
- a known launcher path such as `adams2024_1.bat` or `mdi.bat`

## 2. Minimal run

```powershell
python scripts\adams_batch_pipeline.py `
  --adm E:\path\to\model.adm `
  --output-dir E:\path\to\outputs `
  --config examples\generic_channels.json `
  --launcher E:\path\to\adams2024_1.bat
```

## 3. What you get

After a successful run, the output directory contains:

- solver files: `.acf`, `.res`, `.msg`, `.req`, `.gra`
- channel table: `<prefix>_selected_channels.csv`
- entity catalog: `<prefix>_entity_catalog.csv`
- plot PNG files
- summary markdown: `<prefix>_summary.md`

## 4. Engine-style example

```powershell
python scripts\adams_batch_pipeline.py `
  --adm E:\path\to\engine_model.adm `
  --output-dir E:\path\to\engine_outputs `
  --config examples\engine_channels.json `
  --launcher E:\path\to\adams2024_1.bat
```

## 5. Common failures

- `No ADAMS launcher found`
  Pass `--launcher` explicitly or set `ADAMS_LAUNCHER`.

- solver returns no `.res`
  Check license availability, model validity, and referenced geometry.

- output directory uses non-ASCII path
  This plugin already runs the solver in a temporary ASCII workspace and copies results back.
