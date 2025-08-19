# 🧪 Lab 1 – Pods

## 🎯 Goal
Understand the basics of Kubernetes Pods by creating and running simple workloads.

---

## 📂 Files
.
├── mainfests
│   ├── multi-container-pod.yaml
│   ├── pod-with-config.yaml
│   └── pod.yaml
├── notes.md
└── README.md

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

5.  Testing:

How to run & test

```bash
kubectl apply -f pod.yaml
kubectl get pods
kubectl describe pod nginx-pod
kubectl port-forward pod/nginx-pod 8080:80
```

👉 Then open http://localhost:8080 to see the Nginx welcome page.

---

## 📝 Key Takeaways

- Pods are the smallest deployable unit in Kubernetes.
- A pod can contain one or more containers.
- Pods are ephemeral → if one dies, a Deployment/ReplicaSet is usually needed to respawn it.
- Use kubectl logs and kubectl describe to debug.