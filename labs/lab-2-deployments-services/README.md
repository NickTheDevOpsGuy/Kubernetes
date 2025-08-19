# 🧪 Lab 2 – Deployments & Services

## 🎯 Goal
Learn how Kubernetes manages Pods at scale using **Deployments** and how to expose them with different **Service types** (ClusterIP, NodePort, LoadBalancer).

---

## 📖 Why This Matters
- A **Deployment** ensures the desired number of Pods are running and handles rolling updates.  
- A **Service** provides a stable network identity and load balances traffic to matching Pods.  
- Together, they form the backbone of most real-world Kubernetes applications.  

---

## 📂 Files

```plaintext
.
├── manifests
│   ├── deployment.yaml
│   ├── service-clusterip.yaml
│   ├── service-loadbalancer.yaml
│   └── service-nodeport.yaml
├── notes.md
└── README.md
```

## 🚀 Steps

### 1. Deploy the application

```bash
kubectl apply -f manifests/deployment.yaml
kubectl get deployments
kubectl get pods
```

### 2. Create a ClusterIP Service

```bash
kubectl apply -f manifests/service-clusterip.yaml
kubectl get svc nginx
kubectl get endpoints nginx
```

## 🔎 Confirm endpoints match your Pod IPs:

```bash
kubectl get pods -o wide --show-labels
```

Test inside the cluster:

```bash
kubectl run tmp --rm -it --image=busybox:1.36 -- wget -qO- http://nginx:80
```

### 3. Create a NodePort Service (optional for local clusters)

```bash
kubectl apply -f manifests/service-nodeport.yaml
kubectl get svc nginx-nodeport
```

Then hit:

```bash
http://<node-ip>:<nodeport>
```

(Use kubectl get nodes -o wide to find node IP.)

### 4. Create a LoadBalancer Service (cloud only)

```bash
kubectl apply -f manifests/service-loadbalancer.yaml
kubectl get svc nginx-lb
```

Wait for the EXTERNAL-IP to appear (can take 1–2 minutes). Then open:

```bash
http://<external-ip>:80
```

---

##  Key Takeaways

- Deployment ensures Pod replicas are running and makes upgrades safe.
- ClusterIP = stable internal endpoint for in-cluster communication.
- NodePort = exposes the Service on each Node’s IP at a static port.
- LoadBalancer = provisions a cloud load balancer with a public IP.
- Always ensure labels on Pods match the Service selector.

---

## ⏭️ Next Up

Continue to [Lab 3 – Persistent Storage](../lab-3-persistent-storage) to learn how Kubernetes manages stateful applications with PersistentVolumes and PersistentVolumeClaims.
