# SSF2_Resources

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G31WKOCN)

A comprehensive collection of resources for **Super Smash Flash 2** - the free, browser-based Smash fighting game. Includes installation guides, configuration help, player resources, and community tools.

---

## Quick Start

### For Players
- **New to SSF2?** Start with the **[SSF2 Player Guide](#ssf2-player-guide)** - comprehensive guide covering setup, configuration, online play, replays, and more.
- **Installing on Linux?** Follow [scripts/LINUX_INSTALL_GUIDE.md](scripts/LINUX_INSTALL_GUIDE.md) for step-by-step instructions.
- **Tournament ruleset?** See [Aussie_SSF2_Ruleset.txt](files/Aussie_SSF2_Ruleset.txt).

### For Developers
- Installation script with fallback downloads (3 installation methods supported)
- Test suite for script validation
- Process documentation in `docs/`

---

## SSF2 Player Guide

**Read the full guide here:** [docs/Player_Guide/](docs/Player_Guide/)

A comprehensive guide written by davo1776 covering everything you need to know to play Super Smash Flash 2:

| Section | Coverage |
|---------|----------|
| [1. Setup](docs/Player_Guide/01-setup.md) | Installation on Windows, Mac, Linux, Chromebook; downloading & updating SSF2 |
| [2. Configuration](docs/Player_Guide/02-configuration.md) | Keyboard & controller setup; graphics, sound, and control settings |
| [3. Online Play](docs/Player_Guide/03-online-play.md) | Matchmaking, improving connection, Discord communities, internet checks, error codes |
| [4. Replays](docs/Player_Guide/04-replays.md) | Autosave locations by OS, replay storage scenarios, converting replays to video |
| [5. Resources](docs/Player_Guide/05-resources.md) | General resources, competitive guides, character-specific tools |
| [6. Terminology](docs/Player_Guide/06-terminology.md) | Common fighting game and SSF2-specific terms |
| [7. Remarks](docs/Player_Guide/07-remarks.md) | Final thoughts and acknowledgments |

**Note:** The Player Guide is cloned from an [authoritative Google Doc](https://docs.google.com/document/d/1l5VrAaWmLozu9qnwdjz6MGA9GyurlkgNF8t72eZ4-54) for version control and offline access. See [docs/Player_Guide/README.md](docs/Player_Guide/README.md) for sync details.

---

## Repository Structure

```
scripts/            # Installation scripts and guides
├── INSTALL_SSF2.sh           # Main Linux installer (3 methods: Native, Wine, Wine Portable)
├── TRUST_SSF2_HERE.sh        # Trust script for native Linux installations
└── LINUX_INSTALL_GUIDE.md    # Step-by-step Linux installation guide

files/              # Configuration and reference files
├── Aussie_SSF2_Ruleset.txt   # Community tournament ruleset
└── Super Smash Flash 2 Beta.desktop  # Linux desktop shortcut

docs/               # Documentation
├── Player_Guide/   # Comprehensive player guide (7 sections, 38 images)
├── IDEAS.md        # Development roadmap and improvement ideas
└── HISTORY.md      # Project history and changelog

tests/              # Test suite for script validation
└── test_*.sh       # Individual test scripts
```

---

## Installation Methods

### For Linux Users
The easiest way to install SSF2 on Linux is using the automated script:

```bash
wget https://raw.githubusercontent.com/DavoDC/SSF2_Resources/main/scripts/INSTALL_SSF2.sh
bash INSTALL_SSF2.sh
```

Supports three installation methods:
1. **Native** - Direct native Linux binary (fastest, recommended)
2. **Wine Portable** - Self-contained Wine environment
3. **Wine Installer** - Full Wine installation on your system

For detailed instructions, see [scripts/LINUX_INSTALL_GUIDE.md](scripts/LINUX_INSTALL_GUIDE.md).

### For Windows & Mac
Follow the player guide setup section: [docs/Player_Guide/01-setup.md](docs/Player_Guide/01-setup.md)

---

## Resources Included

- **Tournament Ruleset** - Aussie community competitive ruleset in [files/Aussie_SSF2_Ruleset.txt](files/Aussie_SSF2_Ruleset.txt)
- **Linux Integration** - Desktop shortcut file for Linux users
- **Complete Installation Guide** - Covers Windows, Mac, Linux, Chromebook, and Flatpak
- **Error Code Reference** - Troubleshooting guide for online play errors
- **Controller & Keyboard Setup** - Detailed configuration instructions for all input methods

---

## Development

**Project Status:** Actively maintained (started August 2021)

### Contributing
- Found an issue with the install script? Check [docs/IDEAS.md](docs/IDEAS.md) for known issues
- Run tests with: `bash tests/test_*.sh`
- See [docs/IDEAS.md](docs/IDEAS.md) for the development roadmap and improvement ideas

### Test Suite
The `tests/` directory contains automated test scripts for:
- Dry-run mode validation
- Download fallback functionality
- Script behavior verification

---

## Related SSF2 Projects

- [SSF2Replays](https://github.com/DavoDC/SSF2Replays) - Repository of auto-saved replay files
- [ReplaysAnalyser](https://github.com/DavoDC/ReplaysAnalyser) - Statistical analysis of SSF2 replay data

---

## Support

If you have questions or suggestions:
- **Player Guide:** DM or ping davo1776 on Discord
- **Installation Issues:** Check [scripts/LINUX_INSTALL_GUIDE.md](scripts/LINUX_INSTALL_GUIDE.md) troubleshooting section
- **Feature Ideas:** See [docs/IDEAS.md](docs/IDEAS.md)

---

**Like this project?** Consider supporting the work:
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G31WKOCN)
