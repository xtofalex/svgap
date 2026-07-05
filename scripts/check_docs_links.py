#!/usr/bin/env python3
"""Reject relative documentation links that do not survive the Pages build."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DOCS = (ROOT / "docs").resolve()
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    for document in sorted(DOCS.rglob("*.md")):
        text = document.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            raw = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
            if not raw or raw.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_text = unquote(raw.split("#", 1)[0])
            target = (document.parent / target_text).resolve()
            try:
                target.relative_to(DOCS)
            except ValueError:
                errors.append(
                    f"{document.relative_to(ROOT)}: relative link escapes docs: {raw}; "
                    "use an explicit repository URL"
                )
                continue
            if not target.exists():
                errors.append(
                    f"{document.relative_to(ROOT)}: missing relative link target: {raw}"
                )
    if errors:
        raise SystemExit("\n".join(errors))
    print("documentation links valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
