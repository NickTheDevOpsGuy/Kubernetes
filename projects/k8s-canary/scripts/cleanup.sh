#!/usr/bin/env bash
set -euo pipefail
kubectl delete namespace canary-lab --ignore-not-found
kubectl -n ingress-nginx delete svc ingress-nginx-controller --ignore-not-found || true
helm uninstall ingress-nginx -n ingress-nginx || true
echo "If you created a DOKS cluster for this lab and want to delete it:"
echo "  doctl kubernetes cluster delete k8s-canary-lab"
