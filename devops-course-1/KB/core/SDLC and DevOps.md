# 🧩 SDLC (Software Development Life Cycle)

**SDLC** is the structured process used to design, build, test, and deliver software.

## 🔁 Typical SDLC phases

### 1. **Planning**

* Define goals, scope, timelines
* Identify risks and resources
  👉 Output: roadmap, backlog

---

### 2. **Requirements Analysis**

* Gather functional & non-functional requirements
* Define acceptance criteria
  👉 Output: specs, user stories

---

### 3. **Design**

* Architecture (high-level + low-level)
* Tech stack decisions (e.g. Spring Boot, React, PostgreSQL)
  👉 Output: system design docs, diagrams

---

### 4. **Development**

* Writing code
* Code reviews
* Local testing
  👉 Output: source code

---

### 5. **Testing**

* Unit tests
* Integration tests
* QA validation
  👉 Output: tested build

---

### 6. **Deployment**

* Release to staging/production
* Versioning, rollout strategies
  👉 Output: running system

---

### 7. **Maintenance**

* Bug fixes
* Monitoring
* Improvements
  👉 Output: stable evolving product

---

## 📌 Key idea

SDLC is **linear or iterative process of building software**.

---

# ⚙️ DevOps Lifecycle

**DevOps** extends SDLC by integrating **development + operations + automation + feedback loops**.

It’s not just stages—it’s a **continuous cycle**.

---

## 🔁 DevOps lifecycle stages

### 1. **Plan**

* Backlog, sprint planning
* Tools: Jira, Confluence

---

### 2. **Code**

* Development + version control
* Tools: Git, GitHub/GitLab

---

### 3. **Build**

* Compile, package artifacts
* Tools: Maven, Gradle, Docker

---

### 4. **Test**

* Automated testing
* Tools: JUnit, Selenium

---

### 5. **Release**

* Prepare for deployment
* Versioning, approvals

---

### 6. **Deploy**

* Automated deployment (CI/CD)
* Tools: Kubernetes, Terraform, AWS

---

### 7. **Operate**

* Run application in production
* Scaling, infra management

---

### 8. **Monitor**

* Logs, metrics, alerts
* Tools: Prometheus, Grafana, ELK

---

## 🔄 Continuous loop

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor → (feedback → Plan)
```

---

# 🆚 SDLC vs DevOps (Key Difference)

| Aspect     | SDLC                | DevOps                  |
| ---------- | ------------------- | ----------------------- |
| Nature     | Sequential phases   | Continuous cycle        |
| Focus      | Development process | Delivery + operations   |
| Speed      | Slower releases     | Fast, frequent releases |
| Testing    | Often late stage    | Continuous testing      |
| Deployment | Manual or periodic  | Automated (CI/CD)       |
| Feedback   | Delayed             | Immediate               |

---

# 🧠 How they relate (important insight)

* **SDLC = “what to do”**
* **DevOps = “how to do it continuously and efficiently”**

👉 DevOps **wraps around SDLC** and makes it:

* automated
* iterative
* faster
* safer