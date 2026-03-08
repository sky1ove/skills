# Command Reference

Use `nbdev-help` for the authoritative command list. Use this file as a quick grouping reference.

## Project Setup
- `nbdev-new`: create an nbdev project
- `nbdev-create-config`: create a `pyproject.toml` config file
- `nbdev-install`: install Quarto and the current library
- `nbdev-install-hooks`: install Jupyter and git hooks
- `nbdev-install-quarto`: install Quarto on macOS or Linux

## Notebook And Source Sync
- `nbdev-export`: export notebooks to Python modules
- `nb-export`: export a single notebook
- `nbdev-update`: propagate module changes back to notebooks
- `watch-export`: watch files in `nbs` and export on changes

## Prepare, Clean, Trust, Test
- `nbdev-prepare`: export, test, clean notebooks, and render README when needed
- `nbdev-clean`: strip noisy metadata from notebooks
- `nbdev-trust`: trust notebooks
- `nbdev-test`: run notebook tests in parallel
- `nbdev-fix`: create a working notebook from a conflicted notebook
- `nbdev-merge`: notebook merge driver

## Docs And Site Generation
- `nbdev-docs`: build Quarto docs and `README.md`
- `nbdev-readme`: create `README.md` from the readme notebook
- `nbdev-preview`: preview docs locally
- `nbdev-proc-nbs`: process notebooks for docs rendering
- `nbdev-filter`: Quarto notebook filter
- `nbdev-sidebar`: create `sidebar.yml`
- `nbdev-contributing`: create `CONTRIBUTING.md`

## Versioning And Release
- `nbdev-bump-version`: increment version
- `nbdev-changelog`: create `CHANGELOG.md` from labeled closed issues
- `nbdev-release-gh`: publish a GitHub release flow
- `nbdev-release-git`: tag and create a GitHub release
- `nbdev-release-both`: release conda and PyPI packages
- `nbdev-pypi`: create and upload a PyPI package
- `nbdev-conda`: create a conda `meta.yaml` and optionally build/upload it
- `nbdev-update-license`: update the project license

## Utility
- `nbdev-help`: show help for all console scripts
- `nbdev-requirements`: write `requirements.txt` from `pyproject.toml`
