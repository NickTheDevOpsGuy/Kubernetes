# 🧪 Lab 1 – Pods

## 🎯 Goal
Understand the basics of Kubernetes Pods by creating and running simple workloads.

---

## 📂 Files
- `manifests/pod.yaml` – Basic Nginx pod
- `manifests/multi-container-pod.yaml` – Example pod with multiple containers
- `manifests/pod-with-config.yaml` – Pod using environment variables

---

## 🚀 Steps

1. Apply the pod:
   
   ```bash
   kubectl apply -f manifests/pod.yaml
   ```

2.	Verify it’s running:

    ```bash
    kubectl get pods
    ```

3. Inspect details:  