# SSF2 Resources - Ideas

Ideas for scripts, tools, and improvements across the SSF2 ecosystem.

---

## TIER 0 - BLOCKING (must do before video)

Improve and test the script as much as possible before recording. The video is a showcase - the more polished, the better. Aim to complete all TIER 0 and as many TIER 1 items as practical first.

- **Fix ANSI escape sequences in log file** - script outputs raw color codes to log (e.g. `[0;33m`) when stdout is redirected via tee. Fix: detect if stdout is a file, strip or disable color codes for log output

---

## TIER 1 - SCRIPT IMPROVEMENTS (do before video)

- **`TRUST_SSF2_HERE.sh` - auto-detect correct run location** - script silently writes a useless trust config if run from the wrong folder. Add a pre-check: look for files always present in a native install (e.g. `data/`, `SSF2.x86_64`). If not found, print a clear error and exit.

- **Auto-detect if Wine is installed** - skip Wine menu options entirely if Wine is not present on the system

- **Auto-detect existing SSF2 install and prompt for action** - if SSF2 already installed, show menu: (R)einstall, (Remove) only, (E)xit. Reinstall and Remove must each require double confirmation. Exit needs no confirmation.

- **Better error messages when download fails** - currently silent if wget fails. Show a clear message with the URL that failed.

- **Check for script updates** - compare version header in script against GitHub raw to detect if a newer version is available

- **Mine Discord for common install issues** - trawl the Linux SSF2 Discord community server (manually or programmatically) for recurring problems. Use findings to harden the script: auto-detect architecture, handle known edge cases, improve error messages for real failure modes.

- **Dry-run: show placeholder home path** - bashrc advice currently shows the repo path, not a meaningful simulated path. Show `/home/user/SSF2` placeholder in dry-run mode instead.

- **Dry-run: skip `clear` at startup** - `clear` wipes terminal during dev/testing. Skip it when `DRY_RUN=true`.

- **Dry-run: fix misleading wget skip banner** - `install "wget"` shows a skip banner in dry-run even though wget is unused (curl is used instead). Fix the wording.

---

## SCRIPT AUDIT - INSTALL_SSF2.sh (2026-05-19)

Static analysis of `scripts/INSTALL_SSF2.sh`. Each item tagged `[Severity / Priority]`. Severity = blast radius if it triggers. Priority = do-order (P0 = before video, P3 = nice-to-have). Items marked DUP overlap an existing tier item and are cross-referenced.

### Correctness bugs (real failure modes)

- **No empty-URL guard before download** `[Critical / P0]` - `extractDwlUrl` returns "" if the official page HTML or CDN host changes (the single most likely real-world break). Script then calls `downloadWithFallback ""` -> wget fails cryptically -> `tar -xf` on a missing file -> cascading garbage. Add: if `dwlURL` is empty, print the page URL + chosen pattern and exit 1. Related to existing TIER 1 "Better error messages when download fails" but the root fix is an explicit empty/multi-line check, not just a message.

- **Unquoted paths break on spaces** `[High / P0]` - `mkdir -p $installPath`, `cd $installPath`, `tar -xf $patt_native`, `rm $offURLfile`, `install $1` are all unquoted. Any install folder containing a space (e.g. `My Games`) breaks the install. Very common for GUI users who "Open in Terminal" from a Documents subfolder. Quote all expansions.

- **`cd` failures not checked** `[High / P0]` - `cd $installPath`, `cd SSF2BetaLinux.*/`, `cd SSF2BetaWindows.32bit.*.portable` have no `|| exit`. If the glob does not match (failed download/extract), the script keeps running in the wrong directory: runs `./trust-ssf2.sh` that is not there, prints bashrc advice with the wrong `pwd`. Append `|| { echo "..."; exit 1; }` to every `cd`.

- **No fail-fast (`set -euo pipefail`)** `[High / P1]` - the script plows through every failure (failed apt, failed wget, failed cd). This is the meta-cause behind most cascading-failure items. Add `set -euo pipefail` (with care around the intentional `isNotInstalled` non-zero returns and globs).

- **Download filename vs extract pattern coupling** `[Medium / P1]` - real download uses `wget URL` (server-named file), but extraction uses `tar -xf $patt_native` / `unzip $patt_wine_port` globs. If the CDN's saved filename does not match the regex pattern, extraction silently finds nothing. Download with an explicit `-O` to a known name, or extract the actual downloaded filename.

- **Invalid-choice exits 0** `[Low / P2]` - line ~324 `exit` after "Invalid choice!" returns success. Should be `exit 1` so callers/automation can detect it.

- **`isNotInstalled` has no default case** `[Low / P2]` - if `$PKG_MANAGER` is ever unset/unexpected, the `case` falls through returning 0 (= "not installed"), so `install` always attempts. Add a `*)` arm.

### Cross-distro correctness

- **Universal deps use Debian names on all distros** `[Medium / P1]` - `install "libcanberra-gtk-module"`, `install "libnss3"`, `wine32`, `winbind` are Debian package names but are called unconditionally on dnf/pacman too. The header comment acknowledges this but the script still tries (and silently fails) the install. Map names per `$PKG_MANAGER` or skip+warn on non-apt. DUP-ish of TIER 1 distro support but specifically the universal-deps + wine32/winbind names.

- **`apt update` errors hidden** `[Low / P2]` - `sudo apt update > /dev/null 2>&1` swallows mirror/network failures; Wine install then fails with no clue why. At least keep stderr or print a one-line status.

### Robustness / safety

- **No download integrity check** `[Medium / P2]` - archive is extracted with zero size/checksum validation. A truncated download (Ctrl+C, flaky wifi) yields a corrupt tar/zip and a confusing extract error. Add a minimum-size sanity check or publish+verify a checksum.

- **No cleanup trap** `[Low / P3]` - Ctrl+C mid-run leaves `dwl.html` and partial archives behind (`rm $offURLfile` only runs on the success path). Add a `trap` to clean temp files on exit/interrupt.

- **Partial-download collision on fallback** `[Low / P3]` - if first `wget` writes a partial file then the dot-form fallback runs, wget creates `file.1`; the extract glob can then match the wrong/partial file. Remove the failed partial before retrying.

- **Log files accumulate forever** `[Low / P3]` - every run drops a new `ssf2-install-TIMESTAMP.log` in the launch dir, never pruned. Keep last N, or write into the `SSF2/` folder.

### Stale references / docs

- **Header + issue URL point to old repo** `[Medium / P1]` - usage block (line ~31) tells users to `wget .../DavoDC/LinuxFiles/raw/main/Scripts/SSF2/INSTALL_SSF2.sh` and the unsupported-distro message links `DavoDC/LinuxFiles/issues`. Repo is now `SSF2_Resources`. Users following the embedded instructions fetch from the wrong/stale path. Update both to the current repo.

### Minor / cosmetic

- **`read` without `-r`** `[Low / P3]` - `read chosen_version` and the prompts mangle backslashes; harmless for single letters but bad habit. Use `read -r`.

- **"Press any key" actually needs Enter** `[Low / P3]` - `read -p "Press any key..."` waits for Enter, not any key. Either reword to "Press Enter" or use `read -n1`.

- **`giveBashrcAdvice` nested quotes / mixed indent** `[Low / P3]` - `printYellow "\n    cd "$(pwd)""` has unescaped nested quotes (breaks display if pwd has spaces) and lines ~192-195 mix tabs and spaces. Cosmetic but the printed advice is wrong for spaced paths.

- **Sourcing `/etc/os-release` pollutes script scope** `[Low / P3]` - `. /etc/os-release` injects `NAME`, `VERSION`, `ID`, etc. into the script. No current collision, but fragile if future vars are added. Parse with `grep`/`awk` or run in a subshell.

### General improvements (beyond bug fixes)

- **Pre-flight summary + confirm** - before doing anything, print: detected distro, package manager, chosen version, install path, resolved download URL. One confirmation, then run unattended. Makes failures diagnosable and the video clearer.
- **`--help` / non-interactive flags** - `INSTALL_SSF2.sh --version native --yes` for scripted/CI use and faster repeat testing.
- **Pre-check URL on the real path too** - the dry-run does a HEAD `http_code` check; do the same on Linux before the big download so a bad URL fails in 1s, not after a long timeout.
- **`sudo -v` keepalive upfront** - single early `sudo -v` (refreshed in a background keepalive) instead of multiple scattered password prompts across separate `sudo` calls.
- **shellcheck in CI** - most items above (quoting, unchecked cd, `read -r`, default case) are exactly what `shellcheck` flags. Add a `tests/` shellcheck run so regressions are caught automatically. This is the "fix AND prevent" guard for the whole audit.

---

## TIER 2 - MVP

- **Record YouTube video** (HIGH PRIORITY) - full end-to-end walkthrough for Linux newcomers. Showcase the https://github.com/DavoDC/SSF2_Resources repo, walk through `scripts/LINUX_INSTALL_GUIDE.md` on screen so viewers can follow along using the same doc. Show complete process: downloading the repo, extracting, cd-ing into scripts folder, running the script through all 3 install types. Video description should link to the repo and the guide. Previous video: https://www.youtube.com/watch?v=vHMe8zDKM9A

  Recording plan: on Linux Mint rig, uninstall any existing SSF2, then test each install type in this order - Wine Port, Wine Install, Native (uninstall between each). Combine the ANSI fix user-facing scan with this session. Record a clean final run of all 3 types for the video.

---

## TIER 3 - FUTURE TOOLS

### Host SSF2 Player Guide on GitHub

Player guide lives on Google Drive (https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54/edit). Initial clone to GitHub Wiki or GitHub Pages is a quick win - content hasn't changed in a long time. Link from repo and video description.

---

### SSF2 Online Connection Diagnoser

**Status:** Idea / pre-development. PsnDth replied 2026-04-06: focus on detection only, no auto-fixes. Awaiting FlawTeam (dev_stacks) feedback.

A desktop tool that diagnoses why SSF2 online play isn't working and guides the user through fixes.

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

- **Sync SSF2 player guide from Google Drive to GitHub** - Google Drive doesn't push changes so keeping the GitHub copy up to date needs a scheduled script or manual process.

- **Windows install script** - native Windows equivalent of `INSTALL_SSF2.sh`. Auto-detect 32 vs 64 bit, use mirror version links.

- **AI opponent trained on replay data** - train a model on replay data from https://github.com/DavoDC/SSF2Replays. Smarter AI for people to play against, with online versus support.
