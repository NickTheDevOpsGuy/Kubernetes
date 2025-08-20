# Minikube Notes (optional)
minikube start
minikube addons enable ingress
./scripts/deploy.sh
MINIKUBE_IP=$(minikube ip)
LB_IP=$MINIKUBE_IP ./scripts/test-split.sh
