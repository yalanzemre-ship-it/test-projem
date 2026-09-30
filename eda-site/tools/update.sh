#!/usr/bin/env bash
# Incremental update of the Higgsfield checkout from this repo:
# source overlay, listed images (tools/assets.json), brand files, route tree, typecheck, commit.
# Usage: bash update.sh <checkout_path> <git_ref> "<commit message>"
set -euo pipefail
R="$1"
REF="$2"
MSG="${3:-Site update}"
W=/home/user/work
mkdir -p "$W/fonts"
log() { echo "[$(date +%H:%M:%S)] $*"; }

if ! command -v bun >/dev/null 2>&1 && [ ! -x "$HOME/.bun/bin/bun" ]; then
  curl -fsSL https://bun.sh/install | bash >/dev/null 2>&1
fi
export PATH="$HOME/.bun/bin:$PATH"
python3 -c "import fontTools" 2>/dev/null || pip install -q fonttools >/dev/null 2>&1

log "source"
rm -rf "$W/src" && mkdir -p "$W/src"
curl -fsSL "https://codeload.github.com/yalanzemre-ship-it/test-projem/tar.gz/$REF" | tar -xz -C "$W/src" --strip-components=1
cp -r "$W/src/eda-site/app/." "$R/app/"

log "fonts"
[ -s "$W/fonts/Archivo-VF.ttf" ] || curl -fsSL "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf" -o "$W/fonts/Archivo-VF.ttf"
[ -s "$W/fonts/PlexMono-Medium.ttf" ] || curl -fsSL "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf" -o "$W/fonts/PlexMono-Medium.ttf"
[ -s "$W/fonts/Archivo-XW700.ttf" ] || python3 -m fontTools.varLib.instancer "$W/fonts/Archivo-VF.ttf" wdth=125 wght=700 -o "$W/fonts/Archivo-XW700.ttf" >/dev/null

log "assets"
python3 "$W/src/eda-site/tools/process_v2.py" "$W/src/eda-site/tools/assets.json" "$R" "$W/fonts"

log "deps"
cd "$R/app"
[ -d node_modules ] || bun install >/dev/null 2>&1

log "build (route tree)"
bunx --bun vite build > "$W/build.log" 2>&1 || { tail -40 "$W/build.log"; exit 1; }
log "typecheck"
bunx --bun tsc --noEmit > "$W/tsc.log" 2>&1 || { tail -40 "$W/tsc.log"; exit 1; }

log "commit"
cd "$R"
git add -A
git commit -q -m "$MSG" || true
git log --oneline | head -2
log "DONE"
