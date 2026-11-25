#!/bin/sh
# Render each poster given, in both themes, to PNGs in OUT (default: a temporary directory), with headless Chrome.
# For looking only; nothing in the build reads the PNGs. Usage: tools/look.sh OUT diagrams/M1-*.svg
set -e
out=$1; shift
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
mkdir -p "$out"
for f in "$@"; do
  b=$(basename "$f" .svg)
  w=$(grep -o 'width="[0-9]*"' "$f" | head -1 | tr -dc 0-9)
  h=$(grep -o 'height="[0-9]*"' "$f" | head -1 | tr -dc 0-9)
  for theme in light dark; do
    sed "s/<svg xmlns=/<svg data-theme=\"$theme\" xmlns=/" "$f" > "$out/$b-$theme.svg"
    "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-color-profile=srgb --window-size="$w,$h" \
      --screenshot="$out/$b-$theme.png" "file://$out/$b-$theme.svg" >/dev/null 2>&1
    echo "$out/$b-$theme.png"
  done
done
