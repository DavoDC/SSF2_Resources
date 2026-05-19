# SSF2 Resources - Ideas

Ideas for scripts, tools, and improvements across the SSF2 ecosystem.

Directive: `Claude_Workspace/ClaudeOnly/roadmap/directives/linux-files-yt.md`

Reference video (previous): https://www.youtube.com/watch?v=vHMe8zDKM9A

Video goal: full end-to-end walkthrough for Linux newcomers - showcase the https://github.com/DavoDC/SSF2_Resources repo, show the complete process (downloading the repo, extracting, cd-ing into the scripts folder, running the install script through all 3 install types). Walk through the steps in `scripts/LINUX_INSTALL_GUIDE.md` on screen so viewers can follow along using the same doc. Video description should link to the repo and the guide.

---

## Priority Fixes (before YouTube video)

**Note:** Combine ANSI fix and user-facing scan in one Linux Mint session (both require testing all install types anyway).

### Pre-video checks
- Verify download links and CDN regex patterns still work (URLs live, correct filenames matched)

### Log file ANSI escape sequence issue + major user-facing scan
- Run through each of the 3 install types manually on Linux Mint
- Document any failures, missing dependencies, or unclear prompts
- While testing, check logs for ANSI escape sequence issue and fix if found
- ANSI issue: Script outputs color codes to log file (lines with URLs show `[0;33m` and `[0m` literally)
- Fix: Detect if stdout is redirected to file, disable color codes when logging or strip them on output

---

## Test Plan

### Test Steps

1. Linux Mint rig - uninstall any existing SSF2
2. Run INSTALL_SSF2.sh, choose Native - verify installs and launches
3. Uninstall, run again, choose Wine Install - verify
4. Uninstall, run again, choose Wine Portable - verify
5. Record video during a clean run of all 3

### 3 Install Types (for video demo)

NOTE THIS ORDER:

| Type | Variable | Download | Description |
|------|----------|----------|-------------|
| Wine Port | `wine_port` | `SSF2BetaWindows.32bit.*.portable.zip` | Windows portable via Wine |
| Wine Install | `wine_inst` | `SSF2BetaSetup.32bit.*.exe` | Windows installer via Wine |
| Native | `native` | `SSF2BetaLinux.*.tar` | Linux native build |

Video should demonstrate all 3 types installing successfully.


---

## Future Ideas (post-video)

- **Windows dry-run improvements** (follow-on from DONE feature in HISTORY.md):
  - Bashrc advice shows repo path, not a meaningful simulated path - show `/home/user/SSF2` placeholder in dry-run
  - `clear` at script start clears terminal during dev/testing - skip `clear` when DRY_RUN=true
  - `install "wget"` shows a skip banner even though wget is unused in dry-run mode (curl is used) - minor wording fix

- Auto-detect if Wine is installed and skip Wine menu options if not
- Better error messages if download fails (currently silent?)
- **Auto-detect existing SSF2 install and prompt for action:** If SSF2 already installed, show menu: (R)einstall, (Remove) only, (E)xit. Reinstall and Remove must each have double y/n confirmation gate (not single prompt). Exit needs no confirmation. Better UX than separate uninstall command.
- Support checking for script updates (compare version header against GitHub raw)
- **Mine Discord for common install issues:** Trawl the Linux SSF2 Discord community server (manually or programmatically) for recurring installation problems people report. Use findings to harden the script - e.g. auto-detect architecture, handle edge cases that come up repeatedly, improve error messages for known failure modes. Real user pain points are the best bug tracker.
- **`TRUST_SSF2_HERE.sh` - auto-detect correct run location:** Script only works if run from inside the SSF2 installation folder, but silently does the wrong thing if run elsewhere. Add a pre-check that detects whether native SSF2 is actually installed there by looking for files/folders that are always present in a native install (e.g. `data/`, `SSF2.x86_64` or similar). If not found, print a clear error and exit instead of silently writing a useless trust config.

---

## SSF2 Online Connection Diagnoser (separate tool)

**Status:** Idea / pre-development - PsnDth replied 2026-04-06 (detection only, no auto-fixes). Awaiting FlawTeam (dev_stacks) feedback.

A desktop tool that diagnoses why SSF2 online play isn't working and guides the user through fixes.

- Run automated checks: firewall status, port availability, connection type, ping/speed (Ookla thresholds: ping <=35ms, download >=15 Mbps, upload >=5 Mbps)
- Identify likely causes based on known error codes 000-009
- **Detection and diagnostics only** - report what is wrong, never auto-fix (antivirus flags, user trust). Walk user through manual steps.
- Error 009: P2P impossible (firewall/ISP). Error 004: often paired with opponent 009. "P2P Connection Failed": falls back to MGN relay (USA servers = lag)
- Tech stack: C# CLI app, GUI later if needed
- Full player guide: https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54/edit

### Wireshark + Claude analysis idea
Capture live SSF2 network traffic as .pcap, export via tshark to JSON, have Claude map the protocol - P2P handshake flow, relay fallback detection, port usage. Build a reference model of healthy vs degraded connections to drive the diagnoser's detection logic.

Reference PDFs (in Discord): `Summary: Wireshark Capture Guide for P2P Gaming Troubleshooting.pdf`, `Port Trigger Setup for Gaming Devices.pdf`, `Capture Ports using Wireshark.pdf`
Discord source: https://discord.com/channels/898064250398986262/909616189016260648/1474680695312875560

### Next actions
- [ ] Get feedback from FlawTeam (dev_stacks) - messaged 2026-04-06, awaiting reply
- [ ] Review the 3 PDFs above before designing diagnostic checks
- [ ] Design full diagnostic checks list

---

## Far Future (very low priority)

- **AI opponent trained on replay data** - train a model on replay data from https://github.com/DavoDC/SSF2Replays to create a smarter AI for people to play against, with online versus support
- **Host SSF2 player guide on GitHub** - the player guide currently lives on Google Drive (https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54/edit). Initial clone to GitHub Wiki or GitHub Pages is doable now and useful (content hasn't changed in a long time). Long-term sync between Google Drive and GitHub is a harder problem - Google Drive doesn't push changes automatically, so two-way sync would need a script or manual process. Initial clone is the quick win; live sync is far future.
- **Windows install script** - a native Windows equivalent of `INSTALL_SSF2.sh`. Auto-detect 32 vs 64 bit, use mirror version links. Low priority.
- **ReplaysAnalyser improvements** (https://github.com/DavoDC/ReplaysAnalyser): add summary dashboard / HTML report output; make usable for regular users (VS Installer, installation steps in README, test on secondary machine)
