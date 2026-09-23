# Maintaining eyal-visualization-v2

Maintainer notes. Agents building a dashboard do not need this file.

Willow counts `references/*.md` as references and `assets/*` as assets. HTML starters **must** live in `assets/` (not `examples/`) or Willow shows 0 assets. Agents Read markdown when SKILL.md links it. Copy HTML starters from disk; do not Read them into context.

## Shipping an update

After **any** edit to this skill:

1. Keep `~/.cursor/skills/eyal-visualization-v2` as the working copy.
2. **Bump the version in three places, always together:** [`VERSION`](VERSION), the YAML `version`, and the visible stamp under the h1. A behavior change (new rule, new default, new gate) is a minor bump; wording only is a patch.
3. Run `bash ~/.cursor/skills/eyal-visualization-v2/scripts/ship.sh`. It:
   - refuses to ship if the three version values differ
   - runs `scripts/preship.sh`: the starter must pass `copy-check.py` and `lint_recs.py` on `#view-recommendations` and `#view-overview`
   - syncs `~/.claude/skills/eyal-visualization-v2`
   - pushes to `eyalbou/eyal-visualization-v2` (public, Willow import) and `eyalbou/eyal-personal-skills` (private kit)
4. In Willow: Add Skill / the skill card → **resync From GitHub**. Push does not auto-update Willow.

## Am I on the latest?

```bash
cat ~/.cursor/skills/eyal-visualization-v2/VERSION
gh api repos/eyalbou/eyal-visualization-v2/contents/skills/eyal-visualization-v2/VERSION \
  --jq '.content' | base64 -d
```

Different values mean the local copy is stale: `git pull` the repo, or resync From GitHub in Willow.

## Vendored code

`scripts/deslop.py` is SlopMonster's linter (MIT, Jack Roberts), pinned at commit `f261dbf`. Do not edit it; `lint_recs.py` wraps it. To update, re-copy `tools/deslop.py` from https://github.com/ItsssssJack/SlopMonster and keep the three-line provenance header.
