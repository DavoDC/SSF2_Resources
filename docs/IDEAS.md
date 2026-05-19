# SSF2 Resources - Ideas

Ideas for scripts, tools, and improvements across the SSF2 ecosystem.

---

## TIER 0 - BLOCKING (must fix before video)

Script correctness bugs that will crash the demo or silently corrupt the install for real users. The video is a showcase - every TIER 0 bug is a live failure risk. Fix all of these before recording.

- **Fix ANSI escape sequences in log file** - script outputs raw color codes (e.g. `[0;33m`) when stdout is redirected via tee. Fix: detect if stdout is a terminal, strip or disable color codes when writing to log.

- **No empty-URL guard before download** `[Critical]` - `extractDwlUrl` returns "" if the official page HTML or CDN layout changes. Script then calls `downloadWithFallback ""` -> wget fails cryptically -> `tar -xf` on a missing file -> cascading garbage. Add: if `dwlURL` is empty, print the page URL + chosen pattern and exit 1. This is the single most likely real-world break as the SSF2 site evolves.

- **Unquoted paths break on spaces** `[High]` - `mkdir -p $installPath`, `cd $installPath`, `tar -xf $patt_native`, `rm $offURLfile`, and `install $1` are all unquoted. Any install folder with a space (e.g. `My Games`) breaks the install. Very common for GUI users who "Open in Terminal" from a Documents subfolder. Quote all variable expansions.

- **`cd` failures not checked** `[High]` - `cd $installPath`, `cd SSF2BetaLinux.*/`, and `cd SSF2BetaWindows.32bit.*.portable` have no `|| exit`. If the glob does not match (failed download or extract), the script continues running in the wrong directory: runs `./trust-ssf2.sh` that does not exist there, prints bashrc advice with the wrong `pwd`. Append `|| { echo "..."; exit 1; }` to every `cd`.

- **Stale repo references in script header and issue URL** `[Medium]` - the usage block tells users to `wget .../DavoDC/LinuxFiles/raw/main/Scripts/SSF2/INSTALL_SSF2.sh` (wrong repo) and the unsupported-distro message links `DavoDC/LinuxFiles/issues` (also wrong). Users following the embedded instructions get a 404. Update both to `DavoDC/SSF2_Resources`.

---

## TIER 1 - SCRIPT IMPROVEMENTS (do before video)

### Correctness and robustness fixes

- **No fail-fast (`set -euo pipefail`)** - script plows through every failure (failed apt, failed wget, failed cd). This is the meta-cause behind most cascading-failure issues. Add `set -euo pipefail` with care around intentional non-zero returns in `isNotInstalled` and glob expansions.

- **Universal deps use Debian package names on all distros** - `install "libcanberra-gtk-module"`, `install "libnss3"`, `wine32`, and `winbind` are Debian names but are called unconditionally on dnf/pacman too - silent failures on Fedora/Arch. Map package names per `$PKG_MANAGER` or skip+warn on non-apt.

- **Download filename vs extract pattern coupling** - real download uses `wget URL` (server-named file), but extraction uses `tar -xf $patt_native` / `unzip $patt_wine_port` globs. If the CDN's saved filename does not match the pattern, extraction silently finds nothing. Use `wget -O` to a known name or capture the downloaded filename.

- **No download integrity check** - archive is extracted with zero size/checksum validation. A truncated download (Ctrl+C, flaky wifi) yields a confusing corrupt tar/zip error. Add a minimum-size sanity check; ideally publish and verify a checksum.

- **Better error messages when download fails** - currently silent if wget fails mid-transfer. Show a clear message including the URL that failed and next-step guidance.

- **`apt update` errors hidden** - `sudo apt update > /dev/null 2>&1` swallows mirror/network failures; Wine install then fails with no clue why. Keep stderr or print a one-line status.

- **Invalid-choice exits 0** - bare `exit` after "Invalid choice!" returns success. Should be `exit 1` so callers and automation can detect failure.

- **`isNotInstalled` has no default case** - if `$PKG_MANAGER` is unexpected, the `case` falls through returning 0 (= not installed), causing `install` to always attempt. Add a `*)` arm.

### Functionality improvements

- **`TRUST_SSF2_HERE.sh` - auto-detect correct run location** - script silently writes a useless trust config if run from the wrong folder. Add a pre-check: look for files always present in a native install (e.g. `data/`, `SSF2.x86_64`). If not found, print a clear error and exit.

- **Auto-detect if Wine is installed** - skip Wine menu options entirely if Wine is not present on the system.

- **Auto-detect existing SSF2 install and prompt for action** - if SSF2 already installed, show menu: (R)einstall, (Remove) only, (E)xit. Reinstall and Remove must each require double confirmation.

- **Pre-flight summary + confirm** - before doing anything, print: detected distro, package manager, chosen version, install path, resolved download URL. One confirmation, then run unattended. Makes failures diagnosable and makes the video walkthrough clearer.

- **Pre-check URL reachability before big download** - the dry-run does a HEAD check; do the same on Linux before the actual download so a bad URL fails in 1 second instead of after a long timeout.

- **`sudo -v` keepalive upfront** - a single early `sudo -v` (refreshed in a background loop) avoids multiple password prompts scattered across separate `sudo` calls.

- **Mine Discord for common install issues** - trawl the Linux SSF2 Discord channel for recurring problems. Use findings to harden the script: auto-detect architecture, handle known edge cases, improve error messages for real failure modes.

- **Check for script updates** - compare a version header in the script against GitHub raw to detect if a newer version is available.

### Dry-run fixes

- **Dry-run: show placeholder home path** - bashrc advice currently shows the repo path. Show `/home/user/SSF2` placeholder in dry-run mode instead.

- **Dry-run: skip `clear` at startup** - `clear` wipes the terminal during dev/testing. Skip it when `DRY_RUN=true`.

- **Dry-run: fix misleading wget skip banner** - `install "wget"` shows a dry-run skip banner even though wget is unused in dry-run (curl is used instead). Fix the wording.

### Meta / prevention

- **Add shellcheck to CI** - most correctness items above (unquoted vars, unchecked `cd`, missing `read -r`, no default case) are exactly what shellcheck flags. Add a `tests/` shellcheck run so regressions are caught automatically. This is the fix-and-prevent guard for the whole audit.

- **`--help` / non-interactive flags** - `INSTALL_SSF2.sh --version native --yes` for scripted/CI use and faster repeat testing.

### Cosmetic / minor `[Low priority - polish pass]`

- **"Press any key" actually needs Enter** - `read -p "Press any key..."` waits for Enter, not any key. Reword to "Press Enter" or use `read -n1`.
- **`read` without `-r`** - `read chosen_version` mangles backslashes. Use `read -r`.
- **`giveBashrcAdvice` nested quotes / mixed indent** - `printYellow "\n    cd "$(pwd)""` has unescaped nested quotes (output breaks if pwd contains spaces). Fix quoting and mixed tab/space indent on lines ~192-195.
- **Partial-download collision on fallback** - if first `wget` writes a partial file, the dot-form fallback creates `file.1`; the extract glob can match the partial. Remove the failed partial before retrying.
- **No cleanup trap** - Ctrl+C mid-run leaves `dwl.html` and partial archives behind. Add a `trap` to clean temp files on exit/interrupt.
- **Log files accumulate** - every run drops a new `ssf2-install-TIMESTAMP.log` in the launch dir. Keep last N or move into the `SSF2/` folder.
- **Sourcing `/etc/os-release` pollutes script scope** - `. /etc/os-release` injects `NAME`, `VERSION`, `ID`, etc. No current collision but fragile for future vars. Parse with `grep`/`awk` or run in a subshell.

---

## TIER 2 - MVP

- **Record YouTube video** (HIGH PRIORITY) - full end-to-end walkthrough for Linux newcomers. Showcase the https://github.com/DavoDC/SSF2_Resources repo, walk through `scripts/LINUX_INSTALL_GUIDE.md` on screen so viewers can follow along. Show the complete process: downloading the repo, cd-ing into scripts, running the script through all 3 install types. Video description should link to the repo and the guide. Previous video: https://www.youtube.com/watch?v=vHMe8zDKM9A

  Recording plan: on Linux Mint rig, uninstall any existing SSF2, then test each install type in this order - Wine Port, Wine Install, Native (uninstall between each). Combine the ANSI fix user-facing scan with this session. Record a clean final run of all 3 types for the video.

---

## TIER 3 - FUTURE TOOLS

### Host SSF2 Player Guide on GitHub

Google Drive source: https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54/edit

Full clone of the entire document - all 7 sections in original order, high-quality images preserved. Must stay easy to compare against the Google Doc for future syncing.

**What we have already (in `docs/Player_Guide/RAW/`, gitignored):**
- `SSF2 Player Guide.md` - 2.8MB Google Doc export (best source for conversion)
- `SSF2 Player Guide Site/SSF2PlayerGuide.html` - HTML export
- `SSF2 Player Guide Site/images/` - 38 PNGs, 11MB total (largest: image4.png at 1.5MB)
- `SSF2 Player Guide.pdf` - 12MB PDF (reference only)

**Document structure (7 sections, exact Google Doc order):**
```
1. Setup          (1.1 Installation: Windows/Mac/Linux, 1.2 Download, 1.3 Updating)
2. Configuration  (2.1 Keyboard, 2.2 Controllers, 2.3 Settings/Options)
3. Online Play    (3.1-3.8: matchmaking, errors, P2P, Parsec, Discord)
4. Replays        (4.1 Storage, 4.2 Finding, 4.3 Converting to Video)
5. Resources      (5.1 General, 5.2 Competitive, 5.3 Character-Specific)
6. Terminology
7. Remarks
```

**Target folder layout:**
```
docs/Player_Guide/
  RAW/                   # gitignored - source exports live here
  index.md               # TOC + link to Google Drive source of truth
  images/                # All 38 PNGs at full quality (via Git LFS)
  01-setup.md
  02-configuration.md
  03-online-play.md
  04-replays.md
  05-resources.md
  06-terminology.md
  07-remarks.md
```

Numbered filenames (01-, 02-) mirror Google Doc section numbers - makes side-by-side comparison and future sync diffs easy.

**Images - lossless compression, no Git LFS:**
Google Doc PNG exports are unoptimized (basic encoder, no size effort). `oxipng` (Rust-based, truly lossless - same pixels, better compression) typically saves 30-50% on these. Estimate: 11MB -> ~5-7MB, normal git range.

Run once before committing: `oxipng -o 4 docs/Player_Guide/images/*.png`
(Install: `cargo install oxipng` or grab a binary from https://github.com/shssoichiro/oxipng/releases)

**Conversion process (one-time, from the .md export):**
1. `git lfs install` and add tracking rule for `docs/Player_Guide/images/*.png`
2. Copy images from `RAW/SSF2 Player Guide Site/images/` -> `docs/Player_Guide/images/`
3. Split `RAW/SSF2 Player Guide.md` into 7 section files by heading
4. Fix image refs in each MD: `images/image1.png` style relative paths
5. Write `index.md` with full TOC and Google Drive source link
6. Commit MDs as text + images via Git LFS

**Future sync (when Google Doc is updated):**
Re-export to `RAW/`, re-run split/image-copy, diff the 7 MDs. Numbered filenames + same section order makes the diff readable.

**Link from:** README.md, install script header, video description.

---

### SSF2 Online Connection Diagnoser

**Status:** Idea / pre-development. PsnDth replied 2026-04-06: focus on detection only, no auto-fixes. Awaiting FlawTeam (dev_stacks) feedback.

A desktop tool that diagnoses why SSF2 online play is not working and guides the user through fixes.

- Run automated checks: firewall status, port availability, connection type, ping/speed (Ookla thresholds: ping <=35ms, dl >=15 Mbps, ul >=5 Mbps)
- Identify likely causes from known error codes 000-009
- Detection only - never auto-fix. Walk user through manual steps. (Reason: antivirus flags, user trust)
- Error 009: P2P impossible (firewall/ISP). Error 004: often paired with opponent 009. "P2P Connection Failed": relay fallback via MGN USA servers = lag.
- Tech stack: C# CLI app, GUI later if needed

**Wireshark + Claude analysis sub-idea:** Capture live SSF2 traffic as .pcap, export via tshark to JSON, have Claude map the protocol - P2P handshake, relay fallback, port usage. Build a reference model of healthy vs degraded connections to drive detection logic.

Reference PDFs (in Discord): `Summary: Wireshark Capture Guide for P2P Gaming Troubleshooting.pdf`, `Port Trigger Setup for Gaming Devices.pdf`, `Capture Ports using Wireshark.pdf`
Discord source: https://discord.com/channels/898064250398986262/909616189016260648/1474680695312875560

Next actions:
- [ ] Await FlawTeam (dev_stacks) feedback - messaged 2026-04-06
- [ ] Review the 3 PDFs before designing diagnostic checks
- [ ] Design full diagnostic checks list

---

## TIER 4 - FAR FUTURE (very low priority)

- **Sync SSF2 player guide from Google Drive to GitHub** - Google Drive does not push changes so keeping the GitHub copy up to date needs a scheduled script or manual process.

- **Windows install script** - native Windows equivalent of `INSTALL_SSF2.sh`. Auto-detect 32 vs 64 bit, use mirror version links.

- **AI opponent trained on replay data** - train a model on replay data from https://github.com/DavoDC/SSF2Replays. Smarter AI for people to play against, with online versus support.
