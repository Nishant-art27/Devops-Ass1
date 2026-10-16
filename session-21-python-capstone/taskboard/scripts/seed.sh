#!/usr/bin/env bash
# Create a handful of realistic tasks through the API.
#   BASE_URL=http://localhost:8000 ./scripts/seed.sh
#   BASE_URL=http://taskboard.local CURL_OPTS='--resolve taskboard.local:80:127.0.0.1' ./scripts/seed.sh
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8000}"
post() {
  # shellcheck disable=SC2086
  curl -s ${CURL_OPTS:-} -o /dev/null -w "created %{http_code}\n" -H 'Content-Type: application/json' -X POST "$BASE_URL/api/tasks" -d "$1"
}
post '{"title":"Configure production ingress","description":"Route / and /api through ingress-nginx","priority":"HIGH","assignee":"Nishant","status":"IN_PROGRESS"}'
post '{"title":"Add Grafana dashboard for API latency","description":"p95 per handler, error rate, replicas","priority":"MEDIUM","assignee":"Nishant"}'
post '{"title":"Rotate the PostgreSQL password","description":"Move it into a sealed secret","priority":"HIGH","assignee":"Unassigned"}'
post '{"title":"Write the HPA load test","description":"16 parallel clients for 2 minutes","priority":"LOW","assignee":"Nishant","status":"DONE"}'
post '{"title":"Fix Trivy findings in the frontend image","description":"Bump the nginx base image","priority":"MEDIUM","assignee":"Nishant","status":"DONE"}'
# shellcheck disable=SC2086
curl -s ${CURL_OPTS:-} "$BASE_URL/api/tasks/stats"; echo
