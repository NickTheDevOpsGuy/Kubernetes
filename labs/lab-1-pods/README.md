# 🧪 Lab 1 – Pods

## 🎯 Goal
Understand the basics of Kubernetes Pods by creating and running simple workloads.

---

## 📖 Why Pods Matter
- Pods are the **foundation of Kubernetes** — every workload runs inside a Pod.  
- Even Deployments, DaemonSets, and Jobs are just **controllers that manage Pods**.  
- Understanding Pods helps you debug issues at the lowest level of the cluster.  

---

## 📂 Files
```plaintext
.
├── mainfests
│   ├── multi-container-pod.yaml
│   ├── pod-with-config.yaml
│   └── pod.yaml
├── notes.md
└── README.md
```
---


## 🚀 Steps

### 1. Apply the pod
   
   ```bash
   kubectl apply -f manifests/pod.yaml
   ```

### 2. Verify it’s running

    ```bash
    kubectl get pods
    ```

### 3. Inspect details

    ```bash
    kubectl describe pod nginx-pod
    kubectl logs nginx-pod
    ```

### 4. Test locally

   ```bash
   kubectl port-forward pod/nginx-pod 8080:80
   ```
   
   👉 Then open http://localhost:8080 to see the Nginx welcome page.

### 5.  Cleanup

    ```bash
    k delete pods --all
    ```

---

## 📝 Key Takeaways

- Pods are the smallest deployable unit in Kubernetes.
- A pod can contain one or more containers.
- Pods are ephemeral → if one dies, a Deployment/ReplicaSet is usually needed to respawn it.
- Use kubectl logs and kubectl describe to debug.

---

## ⏭️ Next Up

Head to [Lab 2 – Deployments & Services](../lab-2-deployments-services) to learn how Kubernetes manages Pods at scale and exposes them to the outside world.
