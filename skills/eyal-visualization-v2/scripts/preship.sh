#!/usr/bin/env bash
# The analytics starter must pass the gates the skill makes every dashboard pass.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STARTER="$DIR/../assets/analytics-starter.html"
python3 "$DIR/copy-check.py" "$STARTER" > /dev/null || { python3 "$DIR/copy-check.py" "$STARTER"; exit 1; }
python3 "$DIR/lint_recs.py" "$STARTER" > /dev/null || { python3 "$DIR/lint_recs.py" "$STARTER"; exit 1; }
python3 "$DIR/lint_recs.py" "$STARTER" --id view-overview > /dev/null || { python3 "$DIR/lint_recs.py" "$STARTER" --id view-overview; exit 1; }
FLOW="$DIR/../assets/flow-graph.html"
python3 "$DIR/copy-check.py" "$FLOW" > /dev/null || { python3 "$DIR/copy-check.py" "$FLOW"; exit 1; }
echo "preship: starter passes copy-check, lint_recs (recommendations + overview); flow-graph passes copy-check"
