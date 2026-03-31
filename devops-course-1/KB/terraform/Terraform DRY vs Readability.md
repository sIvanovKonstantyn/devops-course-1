# Problem

Terraform encourages reuse (modules, variables, locals), but overusing DRY leads to:

* Over-abstracted modules that are hard to understand
* Deep variable chains (`var -> local -> module -> output`)
* “Magic” behavior where logic is hidden
* Difficult onboarding for new engineers

At the same time, avoiding DRY completely causes:

* Copy-paste infrastructure
* Configuration drift
* Harder updates across environments

👉 The core problem:
**How do you balance reuse (DRY) with clarity (readability)?**

---

# Solution

## 1. Prefer *Readable Duplication* Over Clever Abstraction

**Bad (too DRY):**

```hcl
module "service" {
  source = "./modules/service"

  for_each = var.services

  name   = each.key
  config = lookup(var.config_map, each.key, {})
}
```

👉 Hard to trace what’s happening.

**Better (slightly duplicated but clear):**

```hcl
module "auth_service" {
  source = "./modules/service"
  name   = "auth"
}

module "payment_service" {
  source = "./modules/service"
  name   = "payment"
}
```

✔ Easier to read
✔ Easier to debug
✔ Safer changes

---

## 2. Use Modules — But Keep Them *Shallow*

**Good module characteristics:**

* Represents a **single responsibility** (e.g., VPC, ECS service)
* Has **clear inputs/outputs**
* Avoids nested modules inside modules (limit depth to 1–2 levels)

**Anti-pattern:**

* “God module” that creates VPC + DB + ECS + IAM

👉 Rule of thumb:

> If a module needs a README to understand → it's too complex

---

## 3. Use `locals` for Clarity, Not Cleverness

**Good:**

```hcl
locals {
  common_tags = {
    project = "my-app"
    env     = var.environment
  }
}
```

**Bad:**

```hcl
locals {
  computed_value = merge(
    var.a,
    var.b,
    { for k, v in var.map : k => upper(v) if contains(keys(var.x), k) }
  )
}
```

👉 If someone has to “parse” it mentally → it’s too complex.

---

## 4. Avoid Over-Parameterization

Too many variables = unreadable modules.

**Bad:**

```hcl
variable "enable_feature_x" {}
variable "feature_x_config" {}
variable "feature_x_override" {}
```

**Better:**

* Split into separate modules OR
* Provide sane defaults

---

## 5. Structure by *Domain*, Not by Type

**Bad structure:**

```
/ec2
/s3
/iam
```

**Good structure:**

```
/networking
/app
/database
```

👉 Think: “What does this system do?” not “What resources does it use?”

---

## 6. Explicit > Implicit

Avoid hidden dependencies:

**Bad:**

```hcl
resource "aws_instance" "app" {
  subnet_id = data.aws_subnet.selected.id
}
```

**Better:**

```hcl
resource "aws_instance" "app" {
  subnet_id = var.subnet_id
}
```

✔ Makes dependencies obvious
✔ Easier testing and reuse

---

## 7. Keep Environments Simple

Avoid extreme DRY like:

```hcl
workspace = terraform.workspace
```

Instead prefer:

```
/envs/dev
/envs/prod
```

👉 Explicit environments reduce surprises.

---

# Commands

### Format code (always do this)

```bash
terraform fmt -recursive
```

### Validate configuration

```bash
terraform validate
```

### Plan changes (review carefully)

```bash
terraform plan
```

### Apply changes

```bash
terraform apply
```

### Show dependency graph (debug complexity)

```bash
terraform graph | dot -Tpng > graph.png
```

---

# Gotchas

## 1. DRY Can Hide Breaking Changes

If multiple services share one module:

* A small change → breaks everything

👉 Solution: version your modules

---

## 2. Overuse of `for_each` and `count`

These reduce duplication but:

* Make plans harder to read
* Complicate debugging

👉 Use only when repetition is **truly dynamic**

---

## 3. Variable Hell

Too many inputs:

* Hard to know what matters
* Hard to test

👉 Keep module interfaces small and opinionated

---

## 4. Implicit Dependencies

Terraform may create resources in wrong order if dependencies are unclear.

👉 Use:

```hcl
depends_on = [...]
```

**only when necessary**

---

## 5. Copy-Paste Isn’t Always Bad

In Terraform:

> ✅ **Duplication is cheaper than wrong abstraction**

---

## Mental Model

* Start **simple and explicit**
* Introduce DRY **only when duplication hurts**
* Optimize for **future readers**, not cleverness