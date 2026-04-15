#!/usr/bin/env bash
set -euo pipefail

PACKAGE_SPEC="${SPARK_RESEARCHER_PACKAGE_SPEC:-git+https://github.com/vibeforge1111/spark-researcher.git}"
APP_NAME="${SPARK_RESEARCHER_APP_NAME:-spark-researcher}"
SKIP_ENSUREPATH="${SPARK_RESEARCHER_SKIP_ENSUREPATH:-0}"

if [[ -n "${SPARK_RESEARCHER_PYTHON:-}" ]]; then
  PYTHON_BIN="$SPARK_RESEARCHER_PYTHON"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python 3.10+ is required." >&2
  exit 1
fi

"$PYTHON_BIN" -m pip install --user --upgrade pip pipx
if [[ "$SKIP_ENSUREPATH" != "1" ]]; then
  "$PYTHON_BIN" -m pipx ensurepath >/dev/null || true
fi
"$PYTHON_BIN" -m pipx uninstall "$APP_NAME" >/dev/null 2>&1 || true
"$PYTHON_BIN" -m pipx install --python "$PYTHON_BIN" "$PACKAGE_SPEC"

cat <<EOF

Installed $APP_NAME.
$(if [[ "$SKIP_ENSUREPATH" != "1" ]]; then printf '%s\n' "If the command is not available yet, open a new shell so pipx's PATH update takes effect."; fi)
To generate a runnable demo without cloning the repo:
  $APP_NAME init --path spark-demo --preset toy --project-name spark-demo
EOF
