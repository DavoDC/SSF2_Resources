# SSF2 Player Guide

This is a GitHub-hosted clone of the original SSF2 Player Guide, written by davo1776.

**Original Google Doc (source of truth):** https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54

The Google Doc is the authoritative version. This clone exists for version control, offline access, and easier linking from the install script and video descriptions.

---

## Contents

| File | Section |
|------|---------|
| [01-setup.md](01-setup.md) | 1. Setup - Installation (Windows, Mac, Linux, Chromebook), Download, Updating |
| [02-configuration.md](02-configuration.md) | 2. Configuration - Keyboard, Controllers, Settings |
| [03-online-play.md](03-online-play.md) | 3. Online Play - Matchmaking, Internet, Errors, P2P, Parsec |
| [04-replays.md](04-replays.md) | 4. Replays - Storage, Finding, Converting to Video |
| [05-resources.md](05-resources.md) | 5. Resources - General, Competitive, Character-Specific |
| [06-terminology.md](06-terminology.md) | 6. Terminology |
| [07-remarks.md](07-remarks.md) | 7. Remarks |
| [images/](images/) | All guide images |

---

## Syncing with the Google Doc

When the Google Doc is updated:
1. Export as Markdown to `RAW/` (gitignored)
2. Split by section and replace the numbered MD files
3. Copy updated images to `images/`, run `oxipng -o 4 images/*.png` for lossless compression
4. Commit the changes

See `docs/IDEAS.md` for the full conversion process.
