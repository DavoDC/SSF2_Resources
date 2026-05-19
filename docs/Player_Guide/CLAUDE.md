# CLAUDE.md - SSF2 Player Guide

Context for Claude when editing or extending this guide.

---

## Origin and purpose

This guide was built by David (davo1776) from real support questions in the McLeod Gaming Discord server. Every troubleshooting entry, misconception correction, and "harmless error" reassurance traces back to a question a real player asked. It is still actively referenced by players every week. It is not a generic reference - it is community-grounded documentation.

Source of truth: https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54

This folder is a clone of that Google Doc, split into sections for GitHub readability. When the Google Doc is updated, re-export and re-sync (see IDEAS.md for process).

---

## What to preserve when editing

**Specificity over generality.** The value of this guide is exact error messages quoted verbatim, exact commands with wildcards explained, exact package names per distro. Do not generalize "install the required libraries" - name them. Do not replace `sudo apt install winbind -y` with "install winbind using your package manager."

**Honest reassurances.** When an error is harmless, say so directly: "These are harmless errors, don't worry, the game will still run normally." This is deliberate. New players panic at terminal output. The reassurance is the point.

**Community attribution.** When a fix came from a specific community member, keep their credit (e.g. "A user said: ... (TheEntertainer#4521)"). This is part of how the guide was built and reflects the collaborative nature of it.

**Misconception corrections.** Sections like the lobby ping note (do not use it, here is what it actually measures) exist because that specific misconception is widespread. Do not soften or remove them.

**Cross-references.** The guide is heavily interlinked. When adding content, link to related sections rather than duplicating. When editing, check that existing cross-references still resolve.

---

## Tone

- Direct and honest, not corporate or over-hedged
- Conversational but precise - matches how David writes in Discord
- Personal recommendations are appropriate ("I personally prefer the Wine version", "I recommend this")
- "I" voice is intentional - this is a community member's guide, not anonymous documentation

---

## What not to do

- Do not remove distro-specific troubleshooting in favour of a generic fallback - the specific fixes are the value
- Do not replace real tool recommendations with "use your preferred tool" - specific recommendations help beginners
- Do not add sections that weren't grounded in real player questions unless explicitly asked
- Do not change the section numbering - it maps to the Google Doc and to the split-MD filenames (01-setup.md etc.)
