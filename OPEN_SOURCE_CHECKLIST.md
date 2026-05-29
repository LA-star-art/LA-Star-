# Open Source Release Checklist

## Before publishing

- Confirm plugin metadata in `.codex-plugin/plugin.json`
- Replace placeholder author information if needed
- Confirm README examples match the final public workflow
- Confirm ADAMS launcher detection works on a clean machine
- Confirm license choice is acceptable
- Remove any local/private model paths from examples

## Functional checks

- Run one end-to-end batch simulation on a clean test model
- Verify `.res` extraction works
- Verify configured plots are generated
- Verify markdown summary is created
- Verify failure behavior when launcher or license is missing

## Packaging checks

- Keep only repo-safe example assets and configs
- Do not publish proprietary ADAMS models unless allowed
- Do not include private result files unless intended as samples

## Suggested next improvements

- add multiple built-in config templates
- add result comparison mode
- add report templating
- add Windows launcher helper docs
