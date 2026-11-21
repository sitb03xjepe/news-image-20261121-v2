#!/usr/bin/env python3
"""Copy the bundled entry.png next to this script into the output folder.

The destination folder comes from MAKEFUN_OUTPUT_DIR and falls back to
/output when that variable is unset. The copy is byte-for-byte.
"""

import os
import shutil
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target_dir / "entry.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
