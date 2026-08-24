#!/usr/bin/env bash
# Push this skill from local to both GitHub copies. Then resync in Willow.
set -euo pipefail

SRC="${EYAL_VIZ_V2_SRC:-$HOME/.claude/skills/eyal-visualization-v2}"
if [[ ! -f "$SRC/SKILL.md" ]]; then
  echo "Missing SKILL.md at $SRC" >&2
  exit 1
fi

ship_to() {
  local repo="$1"
  local dest_rel="$2"
  local tmp
  tmp="$(mktemp -d)"
  git clone --depth 1 "git@github.com:${repo}.git" "$tmp/repo"
  mkdir -p "$tmp/repo/$dest_rel"
  rsync -a --delete --exclude '.git' "$SRC/" "$tmp/repo/$dest_rel/"
  (
    cd "$tmp/repo"
    git add -A
    if git diff --cached --quiet; then
      echo "No changes: $repo"
      return 0
    fi
    git commit -m "Sync eyal-visualization-v2 from local skill."
    git push
    echo "Pushed: $repo"
  )
}

ship_to "eyalbou/eyal-visualization-v2" "skills/eyal-visualization-v2"
ship_to "eyalbou/eyal-personal-skills" "skills/eyal-visualization-v2"
echo "Done. Resync From GitHub in Willow."
