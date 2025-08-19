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
