#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation
"""Generate the catalog index in README.md from per-entry metadata.yaml files.

The index lives between the ``<!-- BEGIN INDEX -->`` and ``<!-- END INDEX -->``
markers in the top-level README. Run without arguments to update the README in
place, or with ``--check`` to fail when the README is out of date (used in CI).
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRIBUTORS_DIR = REPO_ROOT / "contributors"
README_PATH = REPO_ROOT / "README.md"
BEGIN_MARKER = "<!-- BEGIN INDEX -->"
END_MARKER = "<!-- END INDEX -->"

# Maps each contributor sub-directory to the ``kind`` its entries must declare.
KIND_BY_DIR = {
    "agents": "agent",
    "skills": "skill",
    "instructions": "instructions",
}


@dataclass(frozen=True)
class Entry:
    """A single agent or skill discovered from its ``metadata.yaml``."""

    contributor: str
    name: str
    kind: str
    tool: str
    description: str
    tags: tuple[str, ...]
    version: str
    path: str


def _as_str(value: object, default: str = "") -> str:
    return str(value) if value is not None else default


def load_entry(metadata_path: Path) -> Entry:
    """Read one ``metadata.yaml`` file into an :class:`Entry`."""
    with metadata_path.open(encoding="utf-8") as handle:
        raw: object = yaml.safe_load(handle)
    data: dict[str, object] = raw if isinstance(raw, dict) else {}

    contributor = metadata_path.relative_to(CONTRIBUTORS_DIR).parts[0]
    tags_value = data.get("tags")
    tags: tuple[str, ...] = (
        tuple(str(tag) for tag in tags_value) if isinstance(tags_value, list) else ()
    )
    description = " ".join(_as_str(data.get("description")).split())

    return Entry(
        contributor=contributor,
        name=_as_str(data.get("name")) or metadata_path.parent.name,
        kind=_as_str(data.get("kind")),
        tool=_as_str(data.get("tool")),
        description=description,
        tags=tags,
        version=_as_str(data.get("version")),
        path=metadata_path.parent.relative_to(REPO_ROOT).as_posix(),
    )


def collect_entries() -> list[Entry]:
    """Find, validate, and sort every entry under ``contributors/``."""
    if not CONTRIBUTORS_DIR.is_dir():
        return []

    entries: list[Entry] = []
    for path in CONTRIBUTORS_DIR.glob("*/*/*/metadata.yaml"):
        kind_dir = path.relative_to(CONTRIBUTORS_DIR).parts[1]
        expected_kind = KIND_BY_DIR.get(kind_dir)
        if expected_kind is None:
            allowed = ", ".join(sorted(KIND_BY_DIR))
            raise SystemExit(
                f"{path}: unexpected directory '{kind_dir}'; "
                f"entries must live under one of: {allowed}."
            )
        entry = load_entry(path)
        if entry.kind != expected_kind:
            raise SystemExit(
                f"{path}: metadata kind '{entry.kind}' does not match the "
                f"'{kind_dir}' directory (expected kind '{expected_kind}')."
            )
        entries.append(entry)

    return sorted(
        entries, key=lambda entry: (entry.contributor, entry.kind, entry.name)
    )


def render_index(entries: list[Entry]) -> str:
    """Render the entries as grouped Markdown tables."""
    if not entries:
        return "_No agents or skills have been added yet._"

    lines: list[str] = []
    current = ""
    for entry in entries:
        if entry.contributor != current:
            current = entry.contributor
            lines.extend(
                [
                    "",
                    f"### {current}",
                    "",
                    "| Name | Kind | Tool | Description | Tags | Version |",
                    "| --- | --- | --- | --- | --- | --- |",
                ]
            )
        tags = ", ".join(entry.tags)
        lines.append(
            f"| [{entry.name}]({entry.path}) | {entry.kind} | {entry.tool} "
            f"| {entry.description} | {tags} | {entry.version} |"
        )
    return "\n".join(lines).strip()


def update_readme(index: str, *, check: bool) -> bool:
    """Insert ``index`` between the markers. Return True when content changed."""
    text = README_PATH.read_text(encoding="utf-8")
    if BEGIN_MARKER not in text or END_MARKER not in text:
        raise SystemExit(
            f"README.md is missing the {BEGIN_MARKER} / {END_MARKER} markers."
        )

    before, _, rest = text.partition(BEGIN_MARKER)
    _, _, after = rest.partition(END_MARKER)
    new_text = f"{before}{BEGIN_MARKER}\n\n{index}\n\n{END_MARKER}{after}"

    if new_text == text:
        return False
    if not check:
        README_PATH.write_text(new_text, encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if README.md is out of date instead of rewriting it.",
    )
    args = parser.parse_args(argv)

    entries = collect_entries()
    changed = update_readme(render_index(entries), check=bool(args.check))

    if args.check:
        if changed:
            print(
                "README.md index is out of date. Run scripts/generate_index.py.",
                file=sys.stderr,
            )
            return 1
        print("README.md index is up to date.")
        return 0

    if changed:
        print(f"Updated README.md index with {len(entries)} entr(y/ies).")
    else:
        print("README.md index already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
