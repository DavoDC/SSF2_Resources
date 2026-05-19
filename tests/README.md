# Tests

Developer tests for `scripts/INSTALL_SSF2.sh`. Not intended for end users.

Run from any directory:
```bash
bash tests/test_download_fallback.sh
bash tests/test_dry_run.sh
```

Tests use mocked `wget`/`curl` - no network calls, no downloads.
