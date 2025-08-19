# 🧪 Lab 5 – Monitoring & Observability

## 🎯 Goal
Install a cluster monitoring stack with **Prometheus** (metrics), **Alertmanager**, and **Grafana** (dashboards), then explore metrics from nodes, pods, and workloads.

## 📁 Project Structure
```plaintext
.
├── dashboards
│   └── nginx-lab-overview.json
├── helm
│   └── values-prom-stack.yaml
├── mainfests
│   ├── nginx-deployment.yaml
│   └── nginx-service.yaml
├── notes.md
├── queries
│   ├── deployment_nginx_desired_vs_available.promql
│   ├── node_cpu_utilization_percent.promql
│   ├── node_memory_available_percent.promql
│   ├── pod_cpu_rate.promql
│   ├── pod_memory_workingset_mib.promql
│   └── pod_restarts_1h.promql
└── README.md
```

## 🚀 Steps

### 1. Add Helm repo & install the stack

```bash
helm repo update

# Install into a dedicated namespace
helm install monitor prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f helm/values-prom-stack.yaml
```

Check resources:

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

### 2. Access Grafana

```bash
# Get Grafana admin password (release name = monitor)
kubectl get secret -n monitoring monitor-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d; echo

# Port-forward to your laptop
kubectl -n monitoring port-forward svc/monitor-grafana 3000:80
```

###  3. Explore dashboards

In Grafana, look under Dashboards → Browse:

- Kubernetes / Compute Resources / (Node, Namespace, Pod)
- Node Exporter / USE Method
- Kubelet / API Server (varies by chart version)

### 4. Access Prometheus UI

```bash
kubectl -n monitoring port-forward svc/monitor-kube-prometheus-prometheus 9090:9090
```

Open http://localhost:9090 and try some PromQL (see “PromQL Quickstart” below).

### 5. Validate scraping & targets

```bash
# Prometheus should see targets for node-exporter, kube-state-metrics, etc.
kubectl -n monitoring get servicemonitors,podmonitors | head
```

### 6. Cleanup

```bash
helm uninstall monitor -n monitoring
kubectl delete ns monitoring
kubectl delete pods --
```

## 🙋‍♂️ About the Author

- Built with 💻 by [Nicholas Clark](https://www.linkedin.com/in/nickdoesdevops)

- Follow the journey: #NickDoesDevOPS

🧠 #NickDoesDevOps
🚀 #LearningInPublic
🔧 #WorldDominations

- GitHub: [NickTheDevOpsGuy](https://github.com/NickTheDevOpsGuy)

## 📄 License
MIT
