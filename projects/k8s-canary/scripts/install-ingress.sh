#!/usr/bin/env bash
set -euo pipefail
command -v helm >/dev/null 2>&1 || { echo "helm not found. Install Helm first."; exit 1; }

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.publishService.enabled=true \
  --set controller.service.type=LoadBalancer

kubectl -n ingress-nginx rollout status deploy/ingress-nginx-controller
kubectl -n ingress-nginx get svc ingress-nginx-controller
