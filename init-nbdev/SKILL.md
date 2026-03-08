---
name: init-nbdev
description: Create a fresh nbdev project in a new subfolder under a local `git` workspace, backed by a newly created GitHub repository. Use when the user gives a folder or repo name and wants Codex to create and clone the GitHub repo with `gh repo create ... --clone`, create a local uv environment, install `nbdev`, run `nbdev-new`, run `nbdev-install-quarto`, run `nbdev-install-hooks`, run `uv pip install -e ".[dev]"`, and push the initial scaffold to `main`.
---

# Init Nbdev

## Overview

Use this skill to bootstrap a brand new nbdev repository from a folder name inside a local `git` parent folder. Execute the workflow directly instead of explaining it unless the user explicitly asks for a plan only.

## Preconditions

- Confirm the target folder name from the user request.
- Treat the folder name as the GitHub repo name unless the user says otherwise.
- Prefer the authenticated `gh` account for the repo owner unless the user specifies an org or another owner.
- When the repo is being created under a local `git` parent folder, start from that parent directory and let `gh repo create --clone` create the new subfolder.
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
uv pip install -e ".[dev]"
nbdev-clean && nbdev-export
nbdev-prepare
```

7. Commit and push the generated scaffold:

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
