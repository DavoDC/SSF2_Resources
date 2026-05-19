# SSF2 Player Guide - Sync Process

How to keep this GitHub clone in sync with the Google Doc source.

**Google Doc (source of truth):** https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54

---

## Folder layout

```
docs/Player_Guide/
  RAW/                          # gitignored - raw exports live here only
    SSF2 Player Guide.md        # Google Doc -> Download -> Markdown
    SSF2 Player Guide Site/     # Google Doc -> Download -> Web Page (.html)
      SSF2PlayerGuide.html
      images/                   # source PNGs (38 files, ~11MB uncompressed)
  sync/                         # this folder - all sync scripts and docs
    split_guide.py              # splits .md into 7 section files
    compress_images.sh          # copies + losslessly compresses images
    SYNC_PROCESS.md             # this file
  images/                       # committed PNGs (losslessly compressed)
  index.md                      # TOC + Google Drive link
  01-setup.md ... 07-remarks.md # split sections
  CLAUDE.md                     # editing guidance for Claude
  README.md                     # human-facing folder overview
```

---

## Scripts

| Script | Usage |
|--------|-------|
| `compress_images.sh` | `bash docs/Player_Guide/sync/compress_images.sh` |
| `split_guide.py` | `python docs/Player_Guide/sync/split_guide.py` |

Run `compress_images.sh` **before** `split_guide.py` on first setup.
On re-sync, run both - images only need re-running if the guide has new screenshots.

## oxipng setup (REQUIRED for compression)

`compress_images.sh` will fall back to Pillow if oxipng is not found, but **oxipng gives 30-50% better compression**.

**oxipng is NOT committed to git** - it lives in `RAW/` (gitignored). Current location:
```
docs/Player_Guide/RAW/oxipng-10.1.1-x86_64-pc-windows-msvc/oxipng.exe
```

To set up on a new machine:
1. Download from https://github.com/oxipng/oxipng/releases
2. Extract to `docs/Player_Guide/RAW/oxipng-<version>-x86_64-pc-windows-msvc/`
3. `compress_images.sh` will find it automatically (it checks `$PATH` first, then falls back to Pillow)

**IMPORTANT - after compression, verify images match the Google Doc before committing:**
- Open `RAW/SSF2 Player Guide Site/SSF2PlayerGuide.html` in a browser
- Spot-check 3-4 images against the committed `images/` folder
- The HTML export is the authoritative image source - if an image looks wrong in the MD, cross-check the HTML

---

## Initial setup (already done)

1. Exported Google Doc as **Web Page (.html, zipped)** - extracted to `RAW/SSF2 Player Guide Site/`
2. Exported Google Doc as **Markdown (.md)** - saved to `RAW/SSF2 Player Guide.md`
3. Ran `compress_images.sh` - copied 38 PNGs to `images/`, compressed with oxipng
4. Ran `split_guide.py` - split .md into 7 section files + index.md
5. Committed text files and compressed images to git

---

## Re-sync when the Google Doc is updated

```
1. Open Google Doc
2. File -> Download -> Web Page (.html, zipped)
   Extract to: docs/Player_Guide/RAW/SSF2 Player Guide Site/  (overwrite)
3. File -> Download -> Markdown (.md)
   Save to:    docs/Player_Guide/RAW/SSF2 Player Guide.md     (overwrite)
4. bash docs/Player_Guide/sync/compress_images.sh
5. python docs/Player_Guide/sync/split_guide.py
6. git diff docs/Player_Guide/   <-- review what changed
7. git add docs/Player_Guide/
8. git commit -m "sync: update player guide from Google Doc YYYY-MM-DD"
```

The diff in step 6 shows exactly what changed section-by-section - the main benefit of the split format.

---

## Notes

- `RAW/` is gitignored - large exports never touch git
- Images use lossless oxipng compression - no quality loss, ~30-50% smaller
- TOC links in `index.md` use Google Doc anchors - they don't navigate between files (known limitation, fix later if needed)
- The **Web Page export** is the authoritative image source - it extracts PNGs cleanly
- The **Markdown export** is the authoritative text source - cleaner than parsing HTML

---

## Future automation (see IDEAS.md TIER 4)

A future script could chain these steps and commit automatically.
Blocker: Google Docs API needs OAuth - not worth until sync is needed frequently.
