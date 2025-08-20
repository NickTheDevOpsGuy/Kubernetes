#!/usr/bin/env bash
set -euo pipefail
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/app/deployment-v1.yaml
kubectl apply -f k8s/app/deployment-v2.yaml
kubectl apply -f k8s/app/service.yaml
kubectl apply -f k8s/ingress/ingress-stable.yaml
kubectl apply -f k8s/ingress/ingress-canary.yaml
kubectl -n canary-lab get ingress
