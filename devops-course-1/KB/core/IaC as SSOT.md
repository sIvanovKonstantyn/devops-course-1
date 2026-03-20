## 🧠 What is “Single Source of Truth” (SSOT)?

A **Single Source of Truth** is a system where:

* There is **one definitive location** for configuration
* Everything else is **derived from it**
* No hidden/manual/side configurations exist

---

## ⚙️ How IaC fits into this idea

With Infrastructure as Code tools like:

* Terraform
* AWS CloudFormation
* Pulumi

You define infrastructure (servers, networks, databases, etc.) in code files.

👉 That code becomes the **single source of truth**.

---

## 🧩 What it looks like in practice

Instead of:

* Manually creating servers in a cloud console
* Changing configs via SSH
* Forgetting what was changed and when

You do this:

```hcl
resource "aws_instance" "app" {
  ami           = "ami-123456"
  instance_type = "t3.micro"
}
```

That file:

* Defines what should exist
* Is stored in Git
* Is reviewed and versioned

---

## 🔁 Why this is powerful

### 1. Consistency

Every environment (dev/staging/prod) is created from the same code
→ No “works on my machine” problems

---

### 2. Reproducibility

You can:

* Recreate infrastructure from scratch
* Roll back to previous versions

---

### 3. Transparency

All changes are:

* Visible in Git history
* Reviewable via pull requests

---

### 4. No configuration drift

If someone manually changes something:

* IaC tools detect drift
* You can reapply code to fix it

---

### 5. Automation-first mindset

Infrastructure is no longer:

* A manual process
  but:
* A **declarative system**

---

## ⚠️ Important nuance

IaC is only a *true* Single Source of Truth **if**:

* ❌ No manual changes are allowed in the cloud console
* ❌ No “temporary fixes” outside code
* ✅ All changes go through code + CI/CD

Otherwise, you break the SSOT principle.

---

## 🧱 Mental model

Think of IaC like this:

> “The real infrastructure is not what exists in AWS —
> it’s what is defined in the code.”

The cloud is just a **runtime**,
your IaC repo is the **truth**.