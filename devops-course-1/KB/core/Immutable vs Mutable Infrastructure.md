# 🧱 Mutable Infrastructure

**Definition:**
Infrastructure that can be **changed after deployment**.

### 🔧 How it works

* You create a server (VM, container, etc.)
* Later, you **modify it in place**:

  * Install packages
  * Update configs
  * Patch software
  * Restart services

### 📌 Example

* SSH into a server and run:

  ```bash
  apt update && apt install nginx
  ```
* Modify config files manually or via scripts

### ✅ Pros

* Simple and familiar (traditional approach)
* Quick fixes possible (hot patches)
* Lower initial complexity

### ❌ Cons

* **Configuration drift** (servers become inconsistent over time)
* Hard to reproduce environments
* Debugging becomes messy ("it works on one server but not another")
* Risky updates (you modify a running system)

---

# 🧊 Immutable Infrastructure

**Definition:**
Infrastructure that is **never modified after deployment**.
If something needs to change → you **replace it entirely**.

### 🔧 How it works

* Build a **new version** of the server/image
* Deploy it alongside the old one
* Redirect traffic
* Destroy the old version

### 📌 Example

* Build a new Docker image:

  ```bash
  docker build -t app:v2 .
  ```
* Deploy new containers instead of updating existing ones

---

# 🔁 Key Idea

> ❗ You **don’t patch servers** → you **replace them**

---

# ✅ Pros

* **Consistency** (every instance is identical)
* Easy rollback (just switch to previous version)
* No configuration drift
* Better suited for automation and CI/CD

### Common tools & patterns

* Containerization (Docker)
* Image-based deployment (Packer)
* Orchestration (Kubernetes)
* Cloud autoscaling groups

---

# ❌ Cons

* Requires strong automation
* Slower for small quick fixes
* More upfront setup complexity
* Requires good CI/CD pipelines

---

# ⚖️ Comparison

| Feature      | Mutable   | Immutable        |
| ------------ | --------- | ---------------- |
| Updates      | In-place  | Replace entirely |
| Drift        | High risk | None             |
| Rollback     | Hard      | Easy             |
| Debugging    | Harder    | Easier           |
| Speed of fix | Fast      | Slower           |
| Automation   | Optional  | Required         |

---

# 🧠 Real-World Analogy

* **Mutable:**
  Like repairing your car while driving it 🚗🔧

* **Immutable:**
  Like swapping the car for a new one 🚗➡️🚙

---

# 🏗️ When to Use What

### Use Mutable if:

* Small project
* Limited DevOps maturity
* Quick manual fixes needed

### Use Immutable if:

* Production systems
* Microservices architecture
* You use CI/CD pipelines
* You care about reliability and scaling

---

# 💡 Practical Insight (important)

In modern systems (especially with tools like Kubernetes), **immutable infrastructure is the default mindset**.

Even when using VMs:

* Bake images (AMI)
* Deploy via autoscaling
* Avoid SSH access entirely

