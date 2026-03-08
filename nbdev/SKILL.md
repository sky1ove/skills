---
name: nbdev
description: Create, inspect, and maintain current nbdev notebook-driven Python projects. Use when Codex is asked to set up a new nbdev repo, work with `pyproject.toml` and `[tool.nbdev]`, keep notebooks and exported Python in sync, configure Quarto/GitHub Pages docs, troubleshoot nbdev commands or package layout, or prepare and release nbdev packages to GitHub, PyPI, or conda.
---

# Nbdev

## Overview
Use this skill to work on notebook-driven Python repositories that use nbdev or are moving to it. Start with repo inspection, then choose the narrowest workflow that matches the task.

## Core Workflow
1. Inspect the target repo with `scripts/inspect_nbdev_project.py <path> --json`.
2. Classify the repo:
   - `nbdev`: `pyproject.toml` contains `[tool.nbdev]`
   - `unconfigured`: notebooks or Python package exist, but current nbdev config is missing or incomplete
3. Pick the task path:
   - Create a project: use `nbdev-new`, `nbdev-install-quarto`, `nbdev-install-hooks`, then `pip install -e .`
   - Fix or complete config: verify `pyproject.toml`, `[tool.nbdev]`, GitHub Actions, and `lib-path`
   - Sync notebooks and code: prefer `nbdev-prepare`; use `nbdev-clean` plus `nbdev-export` as the lighter fallback
   - Work on docs: use `nbdev-docs`, `nbdev-preview`, `nbdev-readme`, and `_quarto.yml`
   - Release packages: use `nbdev-bump-version`, `nbdev-release-gh`, `nbdev-pypi`, or `nbdev-release-both`
4. Verify the repo state again after making changes when the task affects config, exports, or release metadata.

## Repo Inspection
Run:

```bash
scripts/inspect_nbdev_project.py <path> --json
```

Use the script output to anchor decisions instead of guessing from one file. Treat `project name` and `lib-path` separately; attachment notes explicitly call out repos where the PyPI name differs from the import package name.

## Setup Rules
- Prefer current nbdev config in `pyproject.toml` with `[tool.nbdev]` populated before relying on export or docs automation.
- Keep nbdev installed in the same Python environment as Jupyter and the project.
- Install Quarto before docs work if it is not already available.
- Run `nbdev-install-hooks` in repos that actively edit notebooks to keep notebook metadata and merge behavior clean.
- Recheck `lib-path` after package renames or repo restructuring.

## Daily Development Rules
- Prefer `nbdev-prepare` before pushing when a full export, test, and clean cycle is practical.
- Fall back to `nbdev-clean` and `nbdev-export` when rerunning everything is too expensive.
- Expect CI failures if notebook outputs, exports, and source state drift apart.
- Use `nbdev-update` only for intentional source-to-notebook propagation; otherwise edit the notebook and re-export.

## Docs and Release Rules
- Prefer `_quarto.yml` customization over manually maintaining `sidebar.yml` unless the task specifically requires the file.
- Use GitHub Pages with the `gh-pages` branch for published docs.
- Use `nbdev-release-gh` for changelog-driven GitHub releases and `nbdev-pypi` or `nbdev-release-both` for package publishing.
- Read the release reference before patching around macOS-specific `nbdev-changelog` issues.

## References
- Core commands, setup, and day-to-day workflow: `references/project-workflows.md`
- Docs, sidebar, Quarto, GitHub Pages, and release flow: `references/docs-and-release.md`
- Command grouping and quick lookup: `references/command-reference.md`
- Repo inspection helper: `scripts/inspect_nbdev_project.py`
