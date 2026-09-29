#!/usr/bin/env bash
# Rebuilds the Higgsfield website checkout from this repo in one pass:
# tools, generated images, brand files, source overlay, deps, route tree, typecheck, commit.
# Usage: bash sandbox-build.sh <checkout_path> <git_ref>
set -euo pipefail
R="$1"
REF="$2"
W=/home/user/work
mkdir -p "$W/raw" "$W/fonts"
log() { echo "[$(date +%H:%M:%S)] $*"; }

log "bun"
if ! command -v bun >/dev/null 2>&1 && [ ! -x "$HOME/.bun/bin/bun" ]; then
  curl -fsSL https://bun.sh/install | bash >/dev/null 2>&1
fi
export PATH="$HOME/.bun/bin:$PATH"
pip install -q fonttools >/dev/null 2>&1 || true

log "source"
rm -rf "$W/src" && mkdir -p "$W/src"
curl -fsSL "https://codeload.github.com/yalanzemre-ship-it/test-projem/tar.gz/$REF" | tar -xz -C "$W/src" --strip-components=1

log "downloads"
C=https://d8j0ntlcm91z4.cloudfront.net/user_35Th326p988wTsUijiRXqyjK8MY
i=0
for j in 221533_228c876f-388f-4ba7-a2a6-abb6b3f62983 221533_2a7e5856-2205-4f23-91bc-7307e8b506f2 221533_68c75487-1c05-4cb9-b290-21338610482f 221534_aaea2b7d-857f-4f22-a399-fc6a91fedcf5 221533_fc7e37bb-1fe1-463b-9361-fa1e24348176 221533_e3532775-743c-4daf-95a5-2300449893cb 221534_f249677f-934a-467b-b5cf-8fcb45794e22 221534_69e228b3-b2e9-47b0-8ca8-5e8f16f8ace7; do
  [ -s "$W/raw/board$i.png" ] || curl -fsSL "$C/hf_20260929_$j.png" -o "$W/raw/board$i.png" &
  i=$((i + 1))
done
n=0
for j in 221536_7dedcde7-a33c-476c-b193-44b4a06dcef7 221536_468d0ebc-36e2-4d8e-8fa7-96de3344c982 221536_6ec4abdf-0cf0-4ec8-80a3-4adcfe5f34ed 221536_d8c3a65a-af3e-4efc-a62b-cb715033b070 221536_b010a3ff-ec1f-48db-8f13-c53ba4dedb52 221536_961edf93-3d9d-4115-9347-fe02985291cf 221536_5817d374-0c03-406f-94af-90e5cc2cbc76 221536_9a55fd95-23db-4041-b094-00eab4f326a9 221536_ebc4d5bb-07c8-4541-a6e9-1efc035e66e1 221536_98ebe753-f255-4b42-bb23-6167c74755b5 221536_e3f5fe7e-8db1-4388-9274-66e5b7d127e3 221536_31eeda71-d7a0-4ad3-9c1d-df2e5d24fa47 221539_f87f5c96-5987-4b42-8c90-4c637b12b478 221539_3fbc1902-1016-4da7-95a1-3fbb201f91b8; do
  [ -s "$W/raw/a$n.png" ] || curl -fsSL "$C/hf_20260929_$j.png" -o "$W/raw/a$n.png" &
  n=$((n + 1))
done
[ -s "$W/fonts/Archivo-VF.ttf" ] || curl -fsSL "https://github.com/google/fonts/raw/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf" -o "$W/fonts/Archivo-VF.ttf" &
[ -s "$W/fonts/PlexMono-Medium.ttf" ] || curl -fsSL "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf" -o "$W/fonts/PlexMono-Medium.ttf" &
wait
[ -s "$W/fonts/Archivo-XW700.ttf" ] || python3 -m fontTools.varLib.instancer "$W/fonts/Archivo-VF.ttf" wdth=125 wght=700 -o "$W/fonts/Archivo-XW700.ttf" >/dev/null

log "assets"
python3 "$W/src/eda-site/tools/process_assets.py" "$W/raw" "$R" "$W/fonts"

log "overlay"
cp -r "$W/src/eda-site/app/." "$R/app/"
rm -rf "$R/app/public/presets"
if [ -d "$W/src/eda-site/gallery" ]; then
  mkdir -p "$R/app/public/assets/gallery"
  cp -r "$W/src/eda-site/gallery/." "$R/app/public/assets/gallery/"
fi

log "deps"
cd "$R/app"
bun install >/dev/null 2>&1
grep -q '"gsap"' package.json || bun add gsap@^3.13.0 lenis@^1.3.4 >/dev/null 2>&1

log "route tree + build"
bun run build > "$W/build.log" 2>&1 || { tail -40 "$W/build.log"; exit 1; }
log "typecheck"
bun run typecheck > "$W/tsc.log" 2>&1 || { tail -40 "$W/tsc.log"; exit 1; }

log "commit"
cd "$R"
for p in node_modules dist .output .tanstack .wrangler .nitro; do
  grep -qx "$p" .gitignore 2>/dev/null || grep -qx "/$p" .gitignore 2>/dev/null || echo "$p" >> .gitignore
done
git add -A
git status --short | awk '{print $2}' | cut -d/ -f1-3 | sort | uniq -c | sort -rn | head -20
git commit -q -m "Eda Yalanız Makeup Studio site" || true
git log --oneline | head -3
log "DONE"
