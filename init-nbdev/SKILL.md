---
name: init-nbdev
description: Create a fresh nbdev project in a new subfolder under a local `git` workspace, backed by a newly created GitHub repository. Use when the user gives a folder or repo name and wants Codex to create and clone the GitHub repo with `gh repo create ... --clone`, create a local uv environment, install `nbdev`, run `nbdev-new`, run `nbdev-install-quarto`, run `nbdev-install-hooks`, run `uv pip install -e .`, and push the initial scaffold to `main`.
---

# Init Nbdev

## Overview

Use this skill to bootstrap a brand new nbdev repository from a folder name inside a local `git` parent folder. Execute the workflow directly instead of explaining it unless the user explicitly asks for a plan only.

## Preconditions

- Confirm the target folder name from the user request.
- Treat the folder name as the GitHub repo name unless the user says otherwise.
- Prefer the authenticated `gh` account for the repo owner unless the user specifies an org or another owner.
- Start from the current directory and let `gh repo create --clone` create the new subfolder.
- Refuse to reuse a non-empty target folder unless the user explicitly asks for that.
- Do not modify global git config for this workflow. Rely on cloned repo context and existing git identity.
- Use Apache-2.0 for the repo license by default.

## Workflow

1. Check prerequisites:
   - `gh auth status`
   - `git --version`
   - `python3 --version` or `python --version`
2. Create and clone the GitHub repo in one step from the parent directory:

```bash
gh repo create <owner>/<repo> \
  --public \
  --description "<description>" \
  --license apache-2.0 \
  --clone
```

   - If the user requested a private repo, use `--private` instead of `--public`.
   - If no description was provided, use a short description derived from the repo name.
3. Enter the repo folder created by `--clone`.
4. Create and activate a repo-local uv environment:

```bash
uv venv
source .venv/bin/activate
```

5. Install `nbdev` into that environment:

```bash
uv pip install nbdev
```

6. Run the bootstrap commands in this order:

```bash
nbdev-new
<!-- nbdev-install-quarto --> # run this if successful, otherwise skip
nbdev-install-hooks
uv pip install -e .
```

7. Update `pyproject.toml` under `[tool.nbdev]`:

```toml
title = "<repo>"
lib_path = "<repo>"
```

8. Create `nbs/logo.svg` using the repo name as bold rounded text in a geometric sans style (similar to Fredoka), black letters, minimal modern logo, flat vector design, transparent background.

9. Under `nbs/_quarto.yml`, set the theme and merge these fields into `website.navbar`: if a key overlaps, replace it with the values below; if it does not overlap, keep existing keys and add these new ones.

```yaml
theme:
  - cosmo
  - custom.scss

website:
  favicon: favicon.ico # if not add, can't render the logo in navbar
  navbar:
    title: false
    logo: "logo.svg"
    left:
      - text: "Home"
        href: https://<username>.github.io/<reponame>/
    right:
      - icon: github
        href: "https://github.com/<username>/<reponame>"
  sidebar:
    style: floating
    contents:
      - text: "Get Started"
        href: index.ipynb
      - section: Modules
        contents: "*.ipynb"

metadata-files: [nbdev.yml] # remove sidebar.yml so that sidebar will not show duplicate titles
```

10. Create `nbs/custom.scss` with:

```scss
/*-- scss:defaults --*/

$body-bg: #FFFFFF !default;
$body-color: #000000 !default;
$link-color: #4040BF !default;
$primary: #E8E8FC !default;

$code-bg: null !default; // Placeholder for default value
$code-color: null !default; // Placeholder for default value

$navbar-bg: #5d8ffb !default; // Navbar background color - blue
$navbar-fg: #FFFFFF !default;
$navbar-hl: #000000 !default;

$font-size-root: 18px !default;
```

11. Rewrite `nbs/styles.css` with:

```css
.cell { margin-bottom: 1rem; }
.cell > .sourceCode { margin-bottom: 0; }
.cell-output > pre { margin-bottom: 0; }

.cell-output > pre, .cell-output > .sourceCode > pre, .cell-output-stdout > pre {
  margin-left: 0.8rem;
  margin-top: 0;
  background: none;
  border-left: 2px solid lightsalmon;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.cell-output > .sourceCode { border: none; }

.cell-output > .sourceCode {
  background: none;
  margin-top: 0;
}

div.description {
  padding-left: 2px;
  padding-top: 5px;
  font-size: 1.25rem;
  color: rgba(0, 0, 0, 0.60);
  opacity: 70%;
}


div.sidebar-item-container .active {
  background-color: #E8E8FC;
  color: #000;
}

div.sidebar-item-container a {
  color: #000;
  padding: 4px 6px;
  border-radius: 6px;
  font-size: 1rem;
}

li.sidebar-item {
  margin-top: 3px;
}

span.menu-text {
  line-height: 20px;
}

.navbar-container { max-width: 1282px; }
```

12. Run final prep commands:

```bash
nbdev-clean && nbdev-export
nbdev-prepare
```

13. Commit and push the generated scaffold:

```bash
git add .
git commit -m "init project"
git push
```

## Execution Notes

- If the remote repo already exists, inspect it before continuing. Do not overwrite an existing non-empty remote without explicit user approval.

## Verification

- Confirm `git branch --show-current` is `main`.
- Confirm `git status --short` is empty after the push.
- Confirm `gh repo view <owner>/<repo> --json url,defaultBranchRef` shows the expected URL and `main`.
- Report the repo URL and the initial commit hash in the final response.
