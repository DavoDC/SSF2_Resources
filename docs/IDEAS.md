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
