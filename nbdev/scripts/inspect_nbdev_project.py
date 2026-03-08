#!/usr/bin/env python3
"""Inspect a repository and summarize its nbdev configuration state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


def load_pyproject(pyproject_path: Path) -> dict[str, Any]:
    if not pyproject_path.exists():
        return {}
    if tomllib is not None:
        with pyproject_path.open("rb") as handle:
            return tomllib.load(handle)
    return parse_toml_fallback(pyproject_path.read_text())


def parse_toml_fallback(text: str) -> dict[str, Any]:
    """Parse the small subset of TOML this inspector needs on Python < 3.11."""
    data: dict[str, Any] = {}
    current_path: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        if line.startswith("[") and line.endswith("]"):
            current_path = [part.strip() for part in line[1:-1].split(".")]
            ensure_path(data, current_path)
            continue

        if "=" not in line or not current_path:
            continue

        key, raw_value = line.split("=", 1)
        target = ensure_path(data, current_path)
        target[key.strip()] = parse_toml_value(raw_value.strip())

    return data


def ensure_path(root: dict[str, Any], path_parts: list[str]) -> dict[str, Any]:
    current = root
    for part in path_parts:
        current = current.setdefault(part, {})
    return current


def parse_toml_value(raw_value: str) -> Any:
    if not raw_value:
        return ""

    if raw_value[0] in {'"', "'"} and raw_value[-1] == raw_value[0]:
        return raw_value[1:-1]

    lowered = raw_value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False

    try:
        return int(raw_value)
    except ValueError:
        pass

    return raw_value


def has_nested_mapping(data: dict[str, Any], *path_parts: str) -> bool:
    current: Any = data
    for part in path_parts:
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return isinstance(current, dict)


def detect_state(root: Path) -> dict[str, Any]:
    pyproject_path = root / "pyproject.toml"
    quarto_root = root / "_quarto.yml"
    quarto_nbs = root / "nbs" / "_quarto.yml"
    nbs_dir = root / "nbs"
    workflows_dir = root / ".github" / "workflows"

    pyproject = load_pyproject(pyproject_path)

    tool_nbdev = pyproject.get("tool", {}).get("nbdev", {})
    project_meta = pyproject.get("project", {})

    has_nbdev = has_nested_mapping(pyproject, "tool", "nbdev")
    if has_nbdev:
        state = "nbdev"
    else:
        state = "unconfigured"

    project_name = project_meta.get("name")
    lib_path = tool_nbdev.get("lib-path")
    package_dir_exists = bool(lib_path and (root / lib_path).exists())

    files = {
        "pyproject_toml": pyproject_path.exists(),
        "nbs_dir": nbs_dir.exists(),
        "quarto_root": quarto_root.exists(),
        "quarto_nbs": quarto_nbs.exists(),
        "github_workflows": workflows_dir.exists(),
    }

    recommendations = build_recommendations(
        state=state,
        files=files,
        project_name=project_name,
        lib_path=lib_path,
        package_dir_exists=package_dir_exists,
        nbdev_config_empty=has_nbdev and not tool_nbdev,
    )

    return {
        "root": str(root.resolve()),
        "state": state,
        "files": files,
        "project": {
            "name": project_name,
            "lib-path": lib_path,
            "package_dir_exists": package_dir_exists,
        },
        "recommendations": recommendations,
    }


def build_recommendations(
    *,
    state: str,
    files: dict[str, bool],
    project_name: str | None,
    lib_path: str | None,
    package_dir_exists: bool,
    nbdev_config_empty: bool,
) -> list[str]:
    recommendations: list[str] = []

    if state == "nbdev":
        recommendations.append(
            "Use `nbdev-prepare` before pushing when a full export/test/clean cycle is acceptable; otherwise use `nbdev-clean` plus `nbdev-export`."
        )
    else:
        recommendations.append(
            "If this repo should use nbdev, initialize or configure it with `nbdev-new` or `nbdev-create-config`, then populate `[tool.nbdev]`."
        )

    if project_name and lib_path and project_name != lib_path:
        recommendations.append(
            "Treat the published package name and import package name separately; attachment guidance requires `lib-path` to point at the real Python package directory."
        )

    if nbdev_config_empty:
        recommendations.append(
            "`[tool.nbdev]` exists but is empty. Fill in the nbdev settings before relying on exports, docs, or release automation."
        )

    if lib_path and not package_dir_exists:
        recommendations.append(
            f"`lib-path` is set to `{lib_path}`, but that directory does not exist. Fix the path or create the package directory before exporting."
        )

    if files["nbs_dir"] and not (files["quarto_root"] or files["quarto_nbs"]):
        recommendations.append(
            "Install or configure Quarto before docs work if this repo should publish nbdev docs."
        )

    if files["nbs_dir"] and not files["github_workflows"]:
        recommendations.append(
            "If CI is expected, add or regenerate GitHub workflows after setup."
        )

    return recommendations


def render_text(report: dict[str, Any]) -> str:
    lines = [
        f"root: {report['root']}",
        f"state: {report['state']}",
        "files:",
    ]
    for key, value in report["files"].items():
        lines.append(f"  - {key}: {value}")

    project = report["project"]
    lines.extend(
        [
            "project:",
            f"  - name: {project['name']}",
            f"  - lib-path: {project['lib-path']}",
            f"  - package_dir_exists: {project['package_dir_exists']}",
            "recommendations:",
        ]
    )
    for item in report["recommendations"]:
        lines.append(f"  - {item}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect a repository and summarize its nbdev setup."
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository root to inspect")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        parser.error(f"path does not exist: {root}")
    if not root.is_dir():
        parser.error(f"path is not a directory: {root}")

    report = detect_state(root)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
