#!/usr/bin/env bash
set -euo pipefail
NAME="${1:-k8s-canary-lab}"
REGION="${REGION:-nyc3}"
SIZE="${SIZE:-s-2vcpu-4gb}"
COUNT="${COUNT:-3}"

command -v doctl >/dev/null 2>&1 || { echo "doctl not found. Install it first."; exit 1; }

doctl kubernetes cluster create "$NAME" --region "$REGION" --version latest --size "$SIZE" --count "$COUNT"
doctl kubernetes cluster kubeconfig save "$NAME"
kubectl get nodes
