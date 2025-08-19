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

    ```bash
    kubectl describe pod nginx-pod
    kubectl logs nginx-pod
    ```

4.  Cleanup:

    ```bash
    kubectl delete -f manifests/pod.yaml 
    ```

---

## 📝 Key Takeaways

- Pods are the smallest deployable unit in Kubernetes.
- A pod can contain one or more containers.
- Pods are ephemeral → if one dies, a Deployment/ReplicaSet is usually needed to respawn it.
- Use kubectl logs and kubectl describe to debug.