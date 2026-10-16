#!/usr/bin/env bash
# Generate CPU load on the backend so the HorizontalPodAutoscaler has something to react to.
#   ./scripts/load-test.sh [seconds] [parallel-clients]
#   URL=http://taskboard.local/api/tasks CURL_OPTS='--resolve taskboard.local:80:127.0.0.1' ./scripts/load-test.sh 120 16
set -euo pipefail
URL="${URL:-http://taskboard.local/api/tasks}"
DURATION="${1:-120}"
PARALLEL="${2:-8}"
END=$((SECONDS + DURATION))
echo "Hitting $URL with $PARALLEL clients for ${DURATION}s"
worker() {
  local sent=0
  while [ "$SECONDS" -lt "$END" ]; do
    # shellcheck disable=SC2086
    curl -s -o /dev/null ${CURL_OPTS:-} "$URL" || true
    sent=$((sent + 1))
  done
  echo "client $1 sent $sent requests"
}
for i in $(seq 1 "$PARALLEL"); do worker "$i" & done
wait
echo "Load test completed"
