# 🔁 CI/CD (Continuous Integration / Continuous Delivery)

**CI/CD** is a broader software development practice.

### 🔹 Continuous Integration (CI)

* Developers frequently merge code into a shared repo
* Automated steps:

  * Build
  * Test
  * Lint
* Goal: catch issues early

### 🔹 Continuous Delivery / Deployment (CD)

* Automatically (or semi-automatically) deploy code to environments
* Pipelines push changes to:

  * staging
  * production

### 🧠 Key idea:

> CI/CD pipelines **push changes forward** through environments

### 🛠 Example tools:

* Jenkins
* GitHub Actions
* GitLab CI/CD

---

# 🔄 GitOps

**GitOps is a deployment model**, mostly used with Kubernetes and cloud-native systems.

### 🧠 Key idea:

> Git is the **single source of truth** for both code *and infrastructure*

Instead of pipelines pushing changes, GitOps works like this:

1. You update configuration in Git (e.g., Kubernetes YAML)
2. A controller watches the repo
3. It **pulls changes** and applies them to the cluster

### 🔁 Flow:

* Dev commits → Git repo updated
* GitOps agent detects change
* Agent syncs cluster state with Git

### 🛠 Example tools:

* Argo CD
* Flux

---

# ⚔️ GitOps vs CI/CD — Core Differences

| Aspect             | CI/CD                                  | GitOps              |
| ------------------ | -------------------------------------- | ------------------- |
| Scope              | Broad practice (build + test + deploy) | Deployment strategy |
| Direction          | **Push-based**                         | **Pull-based**      |
| Source of truth    | Pipeline config + code                 | **Git repo only**   |
| Deployment trigger | Pipeline execution                     | Git commit          |
| Infra management   | Optional                               | Core principle      |
| Rollbacks          | Manual or scripted                     | Git revert          |

---

# 🔍 Simple Analogy

* **CI/CD** = Delivery service 🚚
  → Packages (code) get pushed to your house (servers)

* **GitOps** = Smart home system 🏠
  → House constantly checks blueprint (Git) and fixes itself

---

# 🧩 How They Work Together

They’re not competitors—you usually **combine them**:

1. CI pipeline:

   * builds app
   * runs tests
   * creates Docker image

2. Instead of deploying directly:

   * CI updates a Git repo (e.g., Helm chart / manifests)

3. GitOps tool:

   * detects change
   * deploys to Kubernetes

👉 This is the **modern best practice**

---

# ⚡ When to Use What

### Use CI/CD when:

* You need full automation pipeline
* Not using Kubernetes
* Simple deployment flows

### Use GitOps when:

* You use Kubernetes / cloud-native infra
* You want:

  * auditability (everything in Git)
  * easy rollback
  * self-healing systems

---

# 💡 Key Insight

> GitOps doesn’t replace CI/CD—it **redefines CD** (deployment part)
