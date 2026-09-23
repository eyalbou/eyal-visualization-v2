#!/usr/bin/env bash
# Ship this skill: check versions, run preship gates, sync ~/.claude, push to GitHub.
set -euo pipefail

SKILL="eyal-visualization-v2"
REPOS=("eyalbou/eyal-visualization-v2" "eyalbou/eyal-personal-skills")

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -f "$SRC/SKILL.md" ]]; then
  echo "Missing SKILL.md at $SRC" >&2
  exit 1
fi

v_file="$(tr -d '[:space:]' < "$SRC/VERSION")"
v_yaml="$(sed -n 's/^version:[[:space:]]*//p' "$SRC/SKILL.md" | head -1 | tr -d '[:space:]')"
v_stamp="$(grep -o 'Skill version [0-9][0-9.]*' "$SRC/SKILL.md" | head -1 | awk '{print $3}')"
if [[ "$v_file" != "$v_yaml" || "$v_file" != "$v_stamp" ]]; then
  echo "Version mismatch: VERSION=$v_file yaml=$v_yaml stamp=$v_stamp" >&2
  exit 1
fi

if [[ -x "$SRC/scripts/preship.sh" ]]; then
  "$SRC/scripts/preship.sh"
fi

CLAUDE_DEST="$HOME/.claude/skills/$SKILL"
if [[ "$SRC" != "$CLAUDE_DEST" ]]; then
  mkdir -p "$CLAUDE_DEST"
  rsync -a --delete --exclude '.git' --exclude '__pycache__' "$SRC/" "$CLAUDE_DEST/"
  echo "Synced: $CLAUDE_DEST"
fi

ship_to() {
  local repo="$1"
  local tmp
  tmp="$(mktemp -d)"
  git clone --depth 1 "git@github.com:${repo}.git" "$tmp/repo"
  mkdir -p "$tmp/repo/skills/$SKILL"
  rsync -a --delete --exclude '.git' --exclude '__pycache__' "$SRC/" "$tmp/repo/skills/$SKILL/"
  (
    cd "$tmp/repo"
    git add -A
    if git diff --cached --quiet; then
      echo "No changes: $repo"
      return 0
    fi
    git commit -m "Sync $SKILL $v_file from local skill."
    git push
    echo "Pushed: $repo ($v_file)"
  )
}

for repo in "${REPOS[@]}"; do
  ship_to "$repo"
done
echo "Done. Resync From GitHub in Willow."
