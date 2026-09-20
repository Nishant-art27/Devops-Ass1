#!/usr/bin/env bash
# Tears the Nishant App stack down in reverse order.
set -uo pipefail
cd "$(dirname "$0")"
echo "==> Deleting Ingress (nishantapp-ingress)..."
kubectl delete -f ingress.yaml --ignore-not-found
echo "==> Deleting frontend (nishantapp-frontend)..."
kubectl delete -f frontend.yaml --ignore-not-found
echo "==> Deleting backend (nishantapp-backend)..."
kubectl delete -f backend.yaml --ignore-not-found
echo "==> Deleting Secret (nishantapp-db-secret)..."
kubectl delete -f secret.yaml --ignore-not-found
echo "==> Deleting ConfigMap (nishantapp-config)..."
kubectl delete -f configmap.yaml --ignore-not-found
echo "==> Cleanup complete."
