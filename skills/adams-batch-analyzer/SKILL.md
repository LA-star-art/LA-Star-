---
name: adams-batch-analyzer
description: Use for generic ADAMS batch simulation automation, result extraction, configurable plotting, and summary generation for non-interactive solver workflows.
---

# Adams Batch Analyzer

Use this skill when a user wants to automate ADAMS batch simulation, export `.res` results to CSV, or generate plots and summary reports from a model without relying on manual GUI post-processing.

## What this plugin does

- Runs ADAMS solver batch jobs from a `.adm` model
- Auto-generates an `.acf` control file
- Extracts `.res` result data into CSV
- Generates configurable plots from selected entities/channels
- Writes a short markdown summary for the run

## Core script

Run:

```powershell
python <plugin-root>\scripts\adams_batch_pipeline.py `
  --adm <path-to-model.adm> `
  --output-dir <output-folder> `
  --launcher <path-to-adams-launcher-bat-or-mdi.bat> `
  --end-time 2.7 `
  --steps 540 `
  --config <plugin-root>\assets\example_config.json
```

`--launcher` is optional when `ADAMS_LAUNCHER` is set, when the shell already has ADAMS `topdir`, or when ADAMS is installed in a common default location.

## Config model

The config JSON has two sections:

- `channels`
  - `component`: exports a single channel like `MOTION_1.TZ`
  - `vector_magnitude`: computes the magnitude of channels like `FX/FY/FZ`
- `plots`
  - each plot names one or more channel series and an output PNG filename

See:

`<plugin-root>\assets\example_config.json`

## Output files

The pipeline produces:

- `<prefix>.acf`
- `<prefix>.res`
- `<prefix>.msg`
- `<prefix>_entity_catalog.csv`
- `<prefix>_selected_channels.csv`
- configured plot PNGs
- `<prefix>_summary.md`

## Workflow guidance

1. Confirm the user has an `.adm` model and an output directory.
2. If they do not provide a config, either use the example config or create a small task-specific config.
3. Run the batch pipeline script.
4. Read the generated summary and CSV files.
5. Report solver success/failure, key peaks, and where outputs were saved.

## Limitations

- This plugin automates non-interactive batch workflows, not full ADAMS/View GUI editing.
- The model must already be solver-ready and have any required referenced geometry available.
- Different model types may need different channel/plot configs.
- For open-source distribution, document the required ADAMS installation and license setup for the target machine.
