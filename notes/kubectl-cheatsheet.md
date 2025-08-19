# 📝 Kubectl Cheatsheet

Your quick reference for daily Kubernetes commands.  
Because nobody remembers all the flags. 🧠⚡

---

## 🔍 Cluster Info

```bash
kubectl cluster-info              # Show master and services info
kubectl get nodes                 # List all nodes
kubectl describe node <node>      # Show details of a node
kubectl config get-contexts       # List contexts
kubectl config use-context <ctx>  # Switch context
```

## 📦 Pods

```bash
kubectl get pods                  # List all pods
kubectl get pods -o wide          # List pods with more details
kubectl describe pod <pod>        # Show pod details
kubectl logs <pod>                # Show logs from a pod
kubectl exec -it <pod> -- bash    # Exec into a pod
kubectl delete pod <pod>          # Delete a pod
```
---

## 🛠️ Deployments

```bash
kubectl get deployments           # List deployments
kubectl describe deployment <dep> # Show deployment details
kubectl scale deployment <dep> --replicas=3   # Scale replicas
kubectl rollout status deployment <dep>      # Check rollout status
kubectl rollout undo deployment <dep>        # Rollback
```

---

## 🌐 Services

```bash
kubectl get svc                   # List services
kubectl describe svc <service>    # Show service details
kubectl expose deployment <dep> --type=NodePort --port=80
kubectl port-forward svc/<service> 8080:80
```

---

## 📦 Config & Secrets

```bash
kubectl get configmap             # List configmaps
kubectl describe configmap <cfg>  # Show configmap details
kubectl get secret                # List secrets
kubectl describe secret <secret>  # Show secret details
kubectl create secret generic db-secret --from-literal=password=supersecret
```

---

## 💾 Storage

```bash
kubectl get pv                    # List PersistentVolumes
kubectl get pvc                   # List PersistentVolumeClaims
kubectl describe pvc <pvc>        # Show details of a PVC
```

---

## 📅 Jobs & CronJobs

```bash
kubectl get jobs                  # List jobs
kubectl describe job <job>        # Show job details
kubectl get cronjob               # List cronjobs
```

---

## 🕵️ Debugging

```bash
kubectl describe <resource> <name>    # Detailed info
kubectl logs <pod> -c <container>     # Logs for a specific container
kubectl top pod                       # Metrics for pods (needs metrics-server)
kubectl top node                      # Metrics for nodes
```
---

## 🧹 Cleanup

```bash
kubectl delete pod <pod>              # Delete a pod
kubectl delete deployment <dep>       # Delete a deployment
kubectl delete svc <service>          # Delete a service
kubectl delete all --all              # Delete everything in current namespace
```

---

## 🌍 Namespaces

```bash
kubectl get ns                        # List namespaces
kubectl create ns <name>              # Create namespace
kubectl delete ns <name>              # Delete namespace
kubectl config set-context --current --namespace=<ns>
```

---

## ⚡ Shortcuts

```bash
kubectl get po       # Short for pods
kubectl get svc      # Short for services
kubectl get deploy   # Short for deployments
kubectl get ns       # Short for namespaces
```

---

## 🔥 Pro Tip: Alias kubectl to k for speed:

```bash
alias k=kubectl
```

Then you can do things like:

```bash
k get po -A
k describe po mypod
```

---

## 📌 References

- [Kubectl Command Reference](https://kubernetes.io/docs/reference/kubectl/)
