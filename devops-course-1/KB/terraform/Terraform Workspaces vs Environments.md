## Problem

When managing infrastructure with Terraform, you often need multiple isolated setups—like **dev**, **staging**, and **prod**.

The confusion comes from two concepts:

* **Terraform Workspaces**
* **“Environments” (a loose, user-defined concept)**

They sound similar, but they solve different problems and are often misused interchangeably.

---

## Solution

### 1. Terraform Workspaces (state isolation)

**Workspaces = multiple state files for the same configuration**

Terraform workspaces allow you to reuse the **same code**, but maintain **separate state**.

Each workspace:

* Has its own **state file**
* Uses the same `.tf` code
* Can have different variable values

Example use case:

* Same infrastructure pattern deployed per environment (dev/staging/prod)
* Multi-tenant deployments (one config, many instances)

👉 Think of workspaces as:

> “Same blueprint, different saved reality”

---

### 2. Environments (architecture isolation)

**Environments = separate infrastructure stacks**

“Environment” is not a built-in Terraform feature—it’s a **design pattern**.

You typically implement environments by:

* Separate directories (`/dev`, `/staging`, `/prod`)
* Separate backends (different state storage)
* Separate configs and variables

Each environment:

* Can have **different resources**
* Can evolve independently
* Often uses different permissions/accounts

👉 Think of environments as:

> “Different blueprints for different worlds”

---

### Key Difference

| Aspect        | Workspaces            | Environments                       |
| ------------- | --------------------- | ---------------------------------- |
| Scope         | State only            | Full infrastructure                |
| Code          | Same                  | Can differ                         |
| Isolation     | Logical (state-level) | Physical/logical (full separation) |
| Flexibility   | Low–medium            | High                               |
| Typical usage | Simple env separation | Real-world production setups       |

---

## Commands

### Workspace commands

```bash
# List workspaces
terraform workspace list

# Create a new workspace
terraform workspace new dev

# Switch workspace
terraform workspace select dev

# Show current workspace
terraform workspace show
```

### Using workspace in code

```hcl
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket-${terraform.workspace}"
}
```

---

### Environment pattern (directories)

```
infra/
  dev/
    main.tf
    backend.tf
  staging/
    main.tf
  prod/
    main.tf
```

Run per environment:

```bash
cd infra/dev
terraform init
terraform apply
```

---

## Gotchas

### 1. Workspaces are NOT full isolation

* Same backend config (unless you customize it)
* Easy to accidentally apply changes to the wrong workspace
* Not ideal for strict prod separation

👉 Avoid using workspaces alone for production-grade isolation.

---

### 2. Drift risk with shared code

If you rely only on workspaces:

* All environments must evolve together
* Hard to introduce env-specific changes

---

### 3. Backend limitations

Some backends:

* Store all workspace states in one place
* Can become messy or harder to manage

---

### 4. Naming collisions

If you don’t use `terraform.workspace` in naming:

* Resources across workspaces may clash

---

### 5. Teams and permissions

Workspaces:

* Don’t enforce access control per environment

Environments:

* Can map to different cloud accounts (best practice)

---

## Rule of Thumb

* Use **workspaces** when:

  * You need lightweight duplication
  * Infra is identical across environments

* Use **environments (separate configs)** when:

  * You need real isolation
  * Production safety matters
  * Infrastructure differs per stage

