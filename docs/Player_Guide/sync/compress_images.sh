#!/usr/bin/env bash
# compress_images.sh
# Copies PNG images from the RAW site export and losslessly compresses with oxipng.
# Run once during initial setup, then again after each guide re-export.
#
# Usage: bash docs/Player_Guide/sync/compress_images.sh
#
# Requires oxipng for compression (images are copied regardless):
#   cargo install oxipng
#   OR download from: https://github.com/shssoichiro/oxipng/releases

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUIDE_DIR="$(dirname "$SCRIPT_DIR")"
RAW_IMAGES="$GUIDE_DIR/RAW/SSF2 Player Guide Site/images"
OUT_IMAGES="$GUIDE_DIR/images"

if [ ! -d "$RAW_IMAGES" ]; then
    echo "ERROR: RAW images folder not found: $RAW_IMAGES"
    echo "Export the Google Doc as 'Web Page (.html, zipped)' and extract to RAW/"
    exit 1
fi

echo "Copying images from RAW export..."
mkdir -p "$OUT_IMAGES"
cp "$RAW_IMAGES"/*.png "$OUT_IMAGES/"
count=$(ls "$OUT_IMAGES"/*.png | wc -l)
before=$(du -sh "$OUT_IMAGES" | cut -f1)
echo "Copied $count images ($before)."

echo ""
if command -v oxipng &>/dev/null; then
    echo "Running oxipng lossless compression (-o 4)..."
    oxipng -o 4 --quiet "$OUT_IMAGES"/*.png
    after=$(du -sh "$OUT_IMAGES" | cut -f1)
    echo "Done. Size: $before -> $after"
elif command -v python &>/dev/null || command -v python3 &>/dev/null; then
    PY=$(command -v python || command -v python3)
    echo "oxipng not found. Falling back to Pillow lossless optimization..."
    $PY - "$OUT_IMAGES" <<'EOF'
import sys
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    sys.exit(1)
folder = Path(sys.argv[1])
for p in sorted(folder.glob("*.png")):
    img = Image.open(p)
    img.save(p, format="PNG", optimize=True)
print(f"Optimized {len(list(folder.glob('*.png')))} images.")
EOF
    after=$(du -sh "$OUT_IMAGES" | cut -f1)
    echo "Done. Size: $before -> $after"
    echo "NOTE: For better compression (30-50% more), install oxipng and re-run."
    echo "  cargo install oxipng  OR  https://github.com/shssoichiro/oxipng/releases"
else
    echo "WARNING: No compression tool found - images copied uncompressed."
fi

echo ""
echo "Images ready in: $OUT_IMAGES"
