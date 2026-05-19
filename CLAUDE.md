# SSF2_Resources

## Repo structure

- `scripts/` - user-facing files only (INSTALL_SSF2.sh, TRUST_SSF2_HERE.sh, etc.)
- `tests/` - developer tests, not intended for end users
- `files/` - misc SSF2-related files (.desktop shortcuts, rulesets, etc.)
- `docs/` - IDEAS.md and HISTORY.md for the install script

## Conventions

- `scripts/` root is for end users - only files they need to download/run go here
- Tests live in `tests/` at repo root - kept separate so users downloading the script don't see dev scaffolding
- IDEAS and HISTORY: `docs/IDEAS.md` / `docs/HISTORY.md`

## Running tests

See `tests/README.md`.
