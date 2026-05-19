#!/usr/bin/env python3
"""
split_guide.py - Splits the SSF2 Player Guide .md export into 7 numbered section files.

Usage (run from repo root or any location):
    python docs/Player_Guide/sync/split_guide.py

Reads:  docs/Player_Guide/RAW/SSF2 Player Guide.md
Writes: docs/Player_Guide/index.md
        docs/Player_Guide/01-setup.md ... 07-remarks.md

Images are NOT embedded - they reference docs/Player_Guide/images/imageN.png
Run compress_images.sh first to populate that folder.
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent          # sync/
GUIDE_DIR  = SCRIPT_DIR.parent             # Player_Guide/
RAW_MD     = GUIDE_DIR / "RAW/SSF2 Player Guide.md"
OUT_DIR    = GUIDE_DIR

SECTIONS = [
    ("01-setup.md",          1),
    ("02-configuration.md",  2),
    ("03-online-play.md",    3),
    ("04-replays.md",        4),
    ("05-resources.md",      5),
    ("06-terminology.md",    6),
    ("07-remarks.md",        7),
]

# Top-level section heading: # **1\. Title** {#...}
HEADING_RE = re.compile(r'^# \*\*(\d+)\\\.', re.MULTILINE)
# Start of base64 image definitions block (everything after this is dropped)
BASE64_START_RE = re.compile(r'\n\[image\d+\]:\s*<data:image')
# Inline image references: ![][imageN]
IMG_REF_RE = re.compile(r'!\[\]\[image(\d+)\]')


def main():
    if not RAW_MD.exists():
        print(f"ERROR: Source file not found: {RAW_MD}")
        print("Export the Google Doc as Markdown and place it in docs/Player_Guide/RAW/")
        sys.exit(1)

    print(f"Reading {RAW_MD.name} ({RAW_MD.stat().st_size // 1024}KB)...")
    text = RAW_MD.read_text(encoding="utf-8")

    # 1. Fix image refs: ![][image3] -> ![](images/image3.png)
    text = IMG_REF_RE.sub(r'![](images/image\1.png)', text)

    # 2. Truncate at first base64 image definition (multi-line blobs, always at end of file)
    m = BASE64_START_RE.search(text)
    if m:
        text = text[:m.start()]
        print(f"  Stripped base64 definitions starting at char {m.start()}")

    # 3. Find section boundaries
    matches = list(HEADING_RE.finditer(text))
    if len(matches) != 7:
        print(f"WARNING: Expected 7 sections, found {len(matches)}. Check heading format.")

    # 4. Write index.md from preamble (everything before section 1)
    preamble = text[:matches[0].start()].strip()
    index_content = (
        "# SSF2 Player Guide\n\n"
        "**Google Drive source (source of truth):**"
        " https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54\n\n"
        "This is a GitHub-hosted clone split into sections. See [README.md](README.md).\n\n"
        "---\n\n"
        + preamble + "\n"
    )
    write_file(OUT_DIR / "index.md", index_content)

    # 5. Write each section file
    for i, (filename, expected_num) in enumerate(SECTIONS):
        start = matches[i].start()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_text = text[start:end].strip() + "\n"

        actual_num = int(matches[i].group(1))
        if actual_num != expected_num:
            print(f"  WARNING: Expected section {expected_num}, got {actual_num} in {filename}")

        write_file(OUT_DIR / filename, section_text)

    print(f"\nDone. Written to: {OUT_DIR}")


def write_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    size_kb = len(content.encode("utf-8")) // 1024
    print(f"  {path.name:30s} {size_kb:4d}KB")


if __name__ == "__main__":
    main()
