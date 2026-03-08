# Project Workflows

## Detect Repo Shape
- `nbdev`: `pyproject.toml` has `[tool.nbdev]`
- `unconfigured`: no current nbdev config yet, or `[tool.nbdev]` exists but is incomplete

Check package naming carefully when the published package name differs from the import package name. In current nbdev, `lib-path` must point at the real Python package directory.

Example:

```toml
[project]
name = "python-demo"

[tool.setuptools.packages.find]
include = ["demo"]

[tool.nbdev]
title = "demo"
lib-path = "demo"
```

## Create a New Project
Use this flow for a fresh repository:

```bash
git clone <repo-url>
cd <repo-name>
pip install -U nbdev
nbdev-install-quarto
nbdev-new
nbdev-install-hooks
pip install -e .
```

After the first successful prepare/export cycle:

```bash
git add .
git commit -m "initial commit"
git push
```

Enable GitHub Pages on the `gh-pages` branch after docs deployment.

## Run the Daily Workflow
Preferred workflow before pushing:

```bash
pip install -e .
nbdev-prepare
```

Lighter workflow when rerunning the whole notebook set is too expensive:

```bash
nbdev-clean
nbdev-export
```

Keep this constraint in mind: after changing a notebook, rerun it when practical so notebook outputs and exported Python stay consistent with CI.

## Use an Export-Only Pattern
For minimal export-only workflows, mark the module destination in the notebook:

```python
#| default-exp app

#| export
a = 1
```

Add this at the end of the notebook:

```python
from nbdev.export import nb_export
nb_export("notebook_name.ipynb", ".")
```

Import from the generated module with:

```python
from app import *
```

## Manage Environments
- Create a virtual environment with `uv venv`.
- Install nbdev into the same environment used by Jupyter and the project.
- Prefer `uv pip install -e ".[dev]"` or `pip install -e .` for editable local work.
- In existing nbdev repos, prefer `uv pip install <package>` over `uv add` if the workflow assumes editable installs and manual project config.
- Upgrade nbdev with `uv pip install -U nbdev` when the repo already uses `uv`.

Useful shell aliases from the attachment:

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export EDITOR=vim

alias prep='nbdev-clean && nbdev-export'
alias love='source .venv/bin/activate 2>/dev/null || echo "No .venv found in this directory."'
```

## Handle Docs-Only Repos
If the repo is meant only for rendered notebooks and not packaging:
- remove packaging-specific files
- avoid `#| export`
- do not run `nbdev-prepare` or `nbdev-export`
- commit and push notebooks directly for rendered docs

The attachment example removes files such as `setup.py`, `.github/workflows/test.yaml`, and starter notebooks to simplify a docs-only repo.

## Handle Missing Dependencies
Use an import guard when notebooks or workflows should keep running without an optional dependency:

```python
try:
    from package import func
except ImportError as e:
    print(f"package import failed: {e}")
    func = None
```
