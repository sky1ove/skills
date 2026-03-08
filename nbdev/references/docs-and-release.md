# Docs And Release

## Build and Preview Docs
Use these commands for normal docs work:

```bash
nbdev-docs
nbdev-preview
nbdev-readme
```

Use `nbdev-install-quarto` before docs work if Quarto is not installed.

## Configure Quarto
Prefer editing `_quarto.yml` instead of manually maintaining generated sidebar files.

Common customizations from the attachment:
- theme selection
- `custom.scss` for colors
- `styles.css` for typography and layout
- favicon
- navbar links and logo
- sidebar sections and grouping
- `keep-md: true` when markdown output is useful

Example:

```yaml
format:
  html:
    theme:
      - cosmo
      - custom.scss
    css: styles.css
    toc: true
    keep-md: true
```

## Configure Sidebar
Auto-generate `sidebar.yml` only when the repo relies on it:

```bash
nbdev-sidebar
```

Attachment guidance:
- set `custom-sidebar` to `False` before auto-generating
- prefer folder grouping such as `tutorials/*`
- use `index.qmd` inside sections for landing pages when helpful

## Publish Docs
Use GitHub Pages with the `gh-pages` branch.

Typical repo settings flow:
1. Open repository settings.
2. Open Pages.
3. Set the source branch to `gh-pages`.
4. Save and use the deployed site URL as the repo homepage if needed.

## Control Notebook Rendering
Use raw cell front matter to skip execution and showdoc when needed:

```yaml
---
skip_showdoc: true
skip_exec: true
---
```

Hide a notebook from execution and navigation by prefixing the filename with `_`, for example `_02_func.ipynb`.

## Manage Releases
Issue-driven release flow from the attachment:
- label issues as `bug`, `enhancement`, or `breaking`
- create/list issues with `gh issue create` and `gh issue list`
- close issues through commit messages such as `fixes #1`

Release commands:

```bash
nbdev-bump-version
nbdev-release-gh
nbdev-release-both
nbdev-pypi
```

Notes:
- `nbdev-release-gh` updates `CHANGELOG.md` and opens an editor for release note cleanup
- `nbdev-release-both` targets conda and PyPI
- `nbdev-pypi` requires a PyPI API token

Suggested release note sections:

```markdown
### Breaking changes
### New features
### Bugs squashed
```

## Fix Common Publishing Failures
- If the package name is taken on PyPI, rename the package before retrying.
- If upload fails because the version already exists, bump the version before publishing again.
- If repository name and library name differ, verify the published name and `lib-path`/package layout together.

## Add README/Homepage Badges
The attachment calls out:
- Colab buttons via `https://openincolab.com/`
- PyPI badges via Shields.io

Example PyPI badge snippet:

```html
<p><a href="{link to your pypi}"><img src="https://img.shields.io/pypi/v/{your package}" alt="PyPI"></a></p>
```

Avoid blank lines between `<a>` and `<img>` if clean rendering matters.

## Work Around macOS Changelog Failures
If `nbdev-changelog` fails on macOS due to a parallel execution issue, try:

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

If that is still insufficient, the attachment suggests patching `release.py` by replacing the parallel call with a list comprehension:

```python
def _issue_groups(self): return [self._issues(k) for k in self.groups.keys()]
```

Treat that patch as a last resort and prefer fixing the environment first.
