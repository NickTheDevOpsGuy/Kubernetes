# 🧪 Lab 4 – Helm

## 🎯 Goal
Learn how to package, deploy, and manage Kubernetes applications using **Helm charts**.

---

## 📖 Why This Matters
- Helm is the **package manager for Kubernetes**.  
- It simplifies deployments by bundling manifests into reusable **charts**.  
- Helm enables easy **configuration with values.yaml**, and supports **upgrade/rollback** workflows.  
- In real-world DevOps, Helm is often the standard for app delivery into clusters.

---

## 📂 Files
```plaintext
.
├── nginx
│   ├── .helmignore
│   ├── Chart.yaml
│   ├── templates
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── values.yaml
├── notes.md
└── README.md

```

## 🚀 Steps

### 1.  Install Helm (if not already)

```bash
helm version
```
If not installed:
- (Install Helm)[https://helm.sh/docs/intro/install/]

### 2. Create a new chart

```bash
helm create nginx
```

### 3. Customize the chart

- Edit values.yaml to adjust image, replicas, and ports.
- Check templates/deployment.yaml and templates/service.yaml for how values are injected.

### 4. Deploy the chart

```bash
helm install nginx-demo ./nginx
kubectl get all
```

### 5. Upgrade the release

```bash
helm upgrade nginx-demo charts/nginx --set replicaCount=5
kubectl get deploy nginx-demo
```

### 6. Roll back if needed

```bash
helm uninstall nginx-demo
```

---

### 📝 Key Takeaways

- Helm bundles Kubernetes manifests into charts.
- values.yaml provides flexible configuration without editing raw YAML.
- Helm makes upgrades and rollbacks easy.
- Helm charts are widely used in production for apps, operators, and infra tools.

## ⏭️ Next Up

Continue to [Lab 5 – Helm](../lab-5-monitoring-observability) Helm with Metrics, logging, and observability
