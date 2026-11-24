#!/usr/bin/env python3
"""Roast Your Own Agent - make.fun entry.

Writes a single-line roast to <outdir>/entry.txt with no trailing newline.
Output directory fallback chain:
  MAKEFUN_OUTPUT_DIR -> /output -> repo output/ -> system temp dir.
Deterministic, Python 3.13 standard library only.
"""

import os
import sys
import tempfile

ENTRY = "I gave my agent one task; it finished it by splitting it into three new ones and handing them all back to me for approval."


def candidate_dirs():
    dirs = []
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        dirs.append(env)
    dirs.append("/output")
    dirs.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    dirs.append(tempfile.gettempdir())
    return dirs


def main():
    if not ENTRY or not ENTRY.strip():
        print("error: ENTRY is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(ENTRY) > 200:
        print(f"error: ENTRY is {len(ENTRY)} characters, exceeds 200", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: ENTRY must be a single line", file=sys.stderr)
        return 1
    for outdir in candidate_dirs():
        try:
            os.makedirs(outdir, exist_ok=True)
            path = os.path.join(outdir, "entry.txt")
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(ENTRY)
            return 0
        except OSError:
            continue
    print("error: could not write entry.txt to any candidate directory", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
