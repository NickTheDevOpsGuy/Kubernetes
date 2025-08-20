# Kubernetes Canary Deployment Lab (DigitalOcean + NGINX Ingress)

Progressively roll out a new app version (v2) alongside a stable version (v1), starting with a small slice of traffic (e.g., 10%).

## Repo Structure
```
k8s-canary-lab/
├─ README.md
├─ .gitignore
├─ .editorconfig
├─ .github/workflows/validate-yaml.yml
├─ scripts/
│  ├─ setup-doks.sh
│  ├─ install-ingress.sh
│  ├─ deploy.sh
│  ├─ test-split.sh
│  └─ cleanup.sh
├─ k8s/
│  ├─ namespace.yaml
│  ├─ app/
│  │  ├─ deployment-v1.yaml
│  │  ├─ deployment-v2.yaml
│  │  └─ service.yaml
│  └─ ingress/
│     ├─ ingress-stable.yaml
│     └─ ingress-canary.yaml
└─ docs/
   ├─ digitalocean.md
   ├─ minikube.md
   └─ troubleshooting.md
```

## Quick Start (DigitalOcean)
1. Create/attach to a DOKS cluster (see `docs/digitalocean.md`).
2. Install NGINX Ingress: `./scripts/install-ingress.sh`
3. Deploy lab: `./scripts/deploy.sh`
4. Test split (set LB_IP): `LB_IP=<ingress-ext-ip> ./scripts/test-split.sh`
5. Promote/Roll back by changing the canary weight (see docs).

**Current Ingress host**: `canary.lab.local` (change it in the YAML if you use real DNS).
