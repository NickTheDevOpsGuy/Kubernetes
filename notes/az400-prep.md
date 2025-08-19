
# 📘 AZ-400 Prep Notes – Kubernetes

Focused study notes for **Designing and Implementing Microsoft DevOps Solutions (AZ-400)**,  
with emphasis on **Kubernetes & AKS**.

---

## 🎯 Exam Relevance

Kubernetes (AKS in Azure) comes up in several AZ-400 domains:

- **Design & Implement CI/CD Pipelines**  
- **Implement a Monitoring & Feedback Strategy**  
- **Design & Implement Security & Compliance**  
- **Instrument Solutions for Monitoring & Telemetry**  
- **Implement Infrastructure as Code (IaC)**  

---

## 🏗️ Core Concepts to Know

- **Pods / Deployments / Services** → The basic building blocks.  
- **Persistent Volumes (PV) & Persistent Volume Claims (PVC)** → For stateful apps.  
- **ConfigMaps & Secrets** → For externalizing configuration.  
- **Namespaces** → Multi-tenant & environment separation.  
- **Ingress & Load Balancers** → External traffic management.  
- **RBAC & Service Accounts** → Controlling access.  

---

## 🔐 Security & Compliance

- Use **RBAC** to assign least-privilege permissions.  
- Store sensitive values in **Azure Key Vault**, not plain Secrets.  
- **Azure AD Pod Identity** for secure workload identity.  
- Enforce **network policies** for pod communication.  
- Use **Defender for Containers** for runtime security.  

---

## 🚀 CI/CD with AKS

- Deploy to AKS via **Azure DevOps Pipelines** or **GitHub Actions**.  
- Use **kubectl** or **helm** tasks in pipelines.  
- Manage manifests in source control → GitOps principles.  
- Use **multi-environment pipelines** (Dev → Staging → Prod).  
- Automate rollback with **Deployment rollouts**.  

---

## 📊 Monitoring & Feedback

- Enable **Azure Monitor for Containers** on AKS.  
- Integrate with **Application Insights** for app-level telemetry.  
- Use **Log Analytics workspace** for centralized queries.  
- Build **dashboards** for CPU, memory, and request latency.  
- Create **alerts** for pod failures, high latency, or error rates.  

---

## ⚡ Scaling & Reliability

- Configure **liveness probes** and **readiness probes**.  
- Use **Horizontal Pod Autoscaler (HPA)** for scaling based on CPU/memory.  
- Consider **Pod Disruption Budgets (PDBs)** for high availability.  
- Deploy across **Availability Zones** for resilience.  

---

## 💾 Infrastructure as Code (IaC)

- Use **Bicep or Terraform** to provision AKS clusters.  
- Define **networking, RBAC, and monitoring** at deploy time.  
- Parameterize environment values (`dev`, `stage`, `prod`).  
- Automate deployments via **Azure CLI + YAML pipelines**.  

---

## 📚 Sample Exam-Style Questions

1. How do you integrate AKS monitoring with Azure Monitor and App Insights?  
2. What’s the difference between a readiness probe and a liveness probe?  
3. How do you securely inject secrets into a pod running in AKS?  
4. Which IaC tool is recommended for modular and reusable AKS deployments?  
5. How can GitOps improve Kubernetes CI/CD workflows?  

---

## 🔗 References

- [AZ-400 Exam Skills Outline](https://learn.microsoft.com/en-us/certifications/exams/az-400/)  
- [AKS Documentation](https://learn.microsoft.com/en-us/azure/aks/)  
- [Kubernetes Official Docs](https://kubernetes.io/docs/)  
- [Azure Monitor for Containers](https://learn.microsoft.com/en-us/azure/azure-monitor/containers/container-insights-overview)  

---

✍️ *Tip: Pair these notes with your [Kubectl Cheatsheet](kubectl-cheatsheet.md) and actual labs in the `labs/` folder.*  
