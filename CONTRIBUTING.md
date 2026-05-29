# Contributing

## Development goals

This repository aims to provide a generic ADAMS batch analysis workflow rather than a single model-specific automation.

Preferred contribution areas:

- more reusable config templates
- better launcher detection across installations
- comparison mode for multiple result sets
- improved summary/report generation
- better error diagnostics for license, missing geometry, and solver failures

## Local workflow

1. Make changes under `scripts/`, `skills/`, `assets/`, or `examples/`
2. Validate the plugin manifest
3. Run at least one end-to-end batch test with a solver-ready `.adm`
4. Check generated summary and plot outputs

## Validation

Validate plugin structure:

```powershell
python C:\Users\xju\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py E:\codex工作库\adams-batch-analyzer
```

## Contribution guidelines

- Keep the core pipeline generic
- Do not hard-code one specific model structure into the main workflow
- Put model-specific logic into separate example configs or future templates
- Prefer clear failure messages over silent fallback behavior
- Avoid committing proprietary ADAMS models or confidential result files
