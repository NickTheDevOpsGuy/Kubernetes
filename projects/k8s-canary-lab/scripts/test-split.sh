#!/usr/bin/env bash
set -euo pipefail
: "${HOST:=canary.lab.local}"
: "${LB_IP:?Set LB_IP to your ingress EXTERNAL-IP, e.g., LB_IP=167.99.X.X}"
: "${COUNT:=100}"

echo "Hitting http://$HOST via $LB_IP ($COUNT requests)…"
for i in $(seq 1 "$COUNT"); do
  curl -s -H "Host: $HOST" --resolve "$HOST:80:$LB_IP" "http://$HOST/" | grep -Eo 'version: v[12]' || true
done | sort | uniq -c
