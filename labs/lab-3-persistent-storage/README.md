# 🧪 Lab 3 – Persistent Storage

## 🎯 Goal
Learn how to attach **persistent storage** to Pods using **PersistentVolumes (PV)** and **PersistentVolumeClaims (PVC)**.

---

## 📖 Why This Matters
- By default, Pods are **ephemeral** — their data disappears when the Pod is deleted.  
- **PersistentVolumes** provide long-lived storage independent of Pods.  
- **PersistentVolumeClaims** let Pods request storage without caring about the backend.  
- Together, they make stateful workloads possible (databases, file storage, logs, etc.).

---

## 📂 Files
```plaintext
.
├── manifests
│   ├── pv.yaml        # Defines storage (local or cloud provisioned)
│   ├── pvc.yaml       # Claim requesting space
│   └── nginx-pv.yaml  # Pod or Deployment using the claim
├── notes.md
└── README.md
```

---

## 🚀 Steps

### 1. Create a PersistentVolume (PV)

```bash
kubectl apply -f manifests/pv.yaml
kubectl get pv
```

### 2. Create a PersistentVolumeClaim (PVC)

```bash
kubectl apply -f manifests/pvc.yaml
kubectl get pvc
```

## 3. Attach PVC to a Pod/Deployment

```bash
kubectl apply -f manifests/nginx-pv.yaml
kubectl get pods
```

Verify the Pod is running and the volume is mounted:

```bash
kubectl describe pod <pod-name>
```

## 4. Test Persistence

- Write a file inside the Pod (kubectl exec -it <pod> -- sh).
- Delete the Pod.
- Delete the Pod.

### 5. Cleanup

```bash
kubectl delete -f manifests/nginx-pv.yaml
kubectl delete -f manifests/pvc.yaml
kubectl delete -f manifests/pv.yaml
```

## 📝 Key Takeaways

- Pods are ephemeral, but PV + PVC enable persistent state.
- PV = storage resource in the cluster.
- PVC = request for storage by a workload.
- Deployments/Pods mount PVCs to keep data alive across restarts.


## ⏭️ Next Up

Continue to [Lab 4 – Helm](../lab-4-helm) to learn how to package and deploy Kubernetes applications more easily.

