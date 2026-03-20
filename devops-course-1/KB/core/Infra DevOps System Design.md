# 🧱 1. Core DevOps System Design Concerns

### 🔹 Infrastructure

* Where does it run? (cloud, on-prem, hybrid)
* Compute: VMs, containers, serverless
* Networking: VPCs, subnets, load balancers
* Storage: DBs, object storage, caches

👉 Example:

* Amazon Web Services (EC2, S3, RDS)
* Google Cloud Platform
* Microsoft Azure

---

### 🔹 Deployment & CI/CD

* How code moves from dev → prod
* Build, test, deploy automation
* Rollback strategies

👉 Typical flow:

```
Git → CI (build/test) → Artifact → CD → Deploy → Monitor
```

Tools:

* Jenkins
* GitHub Actions
* GitLab CI

---

### 🔹 Containerization & Orchestration

* Packaging services
* Managing scaling & failover

Tools:

* Docker
* Kubernetes

---

### 🔹 Observability

* Logs, metrics, traces
* Alerting & dashboards

Tools:

* Prometheus
* Grafana
* ELK Stack

---

### 🔹 Reliability & Scaling

* Auto-scaling
* Load balancing
* Fault tolerance (multi-AZ, retries, circuit breakers)

---

### 🔹 Security

* Secrets management
* IAM roles
* Network policies
* TLS everywhere

---

# 📦 2. Key Artifacts in DevOps System Design

These are the **deliverables** you produce.

---

### 📄 1. Architecture Diagram

High-level system structure.

Shows:

* Services
* Databases
* Load balancers
* External integrations

---

### 📄 2. Infrastructure as Code (IaC)

Defines infra declaratively.

Tools:

* Terraform
* AWS CloudFormation

Example:

```hcl
resource "aws_instance" "app" {
  instance_type = "t3.micro"
}
```

---

### 📄 3. CI/CD Pipeline Definition

Pipeline config file.

Examples:

* `.github/workflows/*.yml`
* `gitlab-ci.yml`
* `Jenkinsfile`

---

### 📄 4. Deployment Manifests

How apps are deployed.

Example (Kubernetes):

```yaml
apiVersion: apps/v1
kind: Deployment
```

---

### 📄 5. Runbooks

Operational procedures:

* How to restart service
* How to handle incidents
* Debug steps

---

### 📄 6. SLO / SLA Definitions

* Availability targets (e.g. 99.9%)
* Error budgets

---

### 📄 7. Monitoring & Alert Config

* Alert rules
* Dashboards

---

# 📊 3. Diagrams Used in DevOps/System Design

Different diagrams serve different purposes.

---

### 🧭 1. High-Level Architecture Diagram

**Purpose:** Show components & interactions

Tools:

* draw.io
* Lucidchart

---

### 🕸️ 2. Network Diagram

Shows:

* VPC
* Subnets
* Gateways
* Firewalls

---

### 🔄 3. CI/CD Pipeline Diagram

Visualizes:

* Build → Test → Deploy → Release

---

### 📦 4. Deployment Diagram

Focus:

* Pods, containers, nodes
* Scaling strategy

---

### 📈 5. Data Flow Diagram

Shows:

* How data moves through system
* APIs, queues, streams

---

### ⚠️ 6. Failure/Resilience Diagram

Often overlooked but very important:

* What happens if:

  * DB goes down?
  * Service crashes?
  * Region fails?

---

# 🛠️ 4. Supporting Tools (DevOps Stack)

### Infrastructure & Config

* Ansible
* Pulumi

### Secrets

* HashiCorp Vault

### Service Mesh (advanced)

* Istio

---

# 🧠 5. How to Think About It (Mental Model)

When designing from DevOps perspective, always answer:

### 1. How is it deployed?

* One-click deploy?
* Zero downtime?

### 2. How does it scale?

* Horizontal? Auto-scaling?

### 3. What breaks?

* Single points of failure?

### 4. How do we detect issues?

* Metrics? Alerts?

### 5. How do we recover?

* Rollback? Self-healing?

---

# 🔥 Example (Simple Service)

Let’s say you design a REST API:

* Containerized with Docker
* Runs on Kubernetes
* Exposed via Load Balancer
* Uses PostgreSQL
* CI/CD via GitHub Actions
* Monitoring via Prometheus + Grafana

Artifacts:

* `Dockerfile`
* `k8s deployment.yaml`
* `terraform/main.tf`
* `.github/workflows/deploy.yml`
* dashboards + alerts

Diagrams:

* Architecture diagram
* Deployment diagram
* CI/CD pipeline diagram

---

# ✅ Summary

From a DevOps/Infra perspective, system design is about:

* **Running the system** (infra, containers)
* **Shipping the system** (CI/CD)
* **Observing the system** (logs, metrics)
* **Protecting the system** (security, resilience)

Artifacts = *code + configs + docs*
Diagrams = *visual explanation of those systems*

