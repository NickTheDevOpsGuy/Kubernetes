# DigitalOcean Setup

## Create Cluster
doctl auth init
doctl kubernetes cluster create k8s-canary-lab --region nyc3 --version latest --size s-2vcpu-4gb --count 3
doctl kubernetes cluster kubeconfig save k8s-canary-lab
kubectl get nodes

## Install Ingress (NGINX)
./scripts/install-ingress.sh
kubectl -n ingress-nginx get svc ingress-nginx-controller  # note EXTERNAL-IP

## Deploy Lab
./scripts/deploy.sh

## Test Split
LB_IP=<EXTERNAL-IP> ./scripts/test-split.sh  # counts v1/v2 responses

## Promote / Roll Back
kubectl -n canary-lab annotate ingress app-canary nginx.ingress.kubernetes.io/canary-weight="50" --overwrite  # promote
kubectl -n canary-lab annotate ingress app-canary nginx.ingress.kubernetes.io/canary-weight="0" --overwrite   # rollback

## Cleanup
./scripts/cleanup.sh
