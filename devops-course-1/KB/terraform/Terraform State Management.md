# Problem

Terraform needs to track **what it created** vs **what exists now**.
This is stored in a file called **state (`terraform.tfstate`)**.

Without proper state management:

* ❌ **Team conflicts**
  Multiple developers run `terraform apply` → overwrite each other’s changes

* ❌ **Drift & inconsistency**
  Local state becomes outdated → Terraform makes wrong decisions

* ❌ **No concurrency control**
  Two applies at the same time → corrupted infrastructure

* ❌ **Secrets exposure**
  State file often contains sensitive data (passwords, ARNs, etc.)

👉 Local state works only for **solo development**, not for teams.

---

# Solution

## 1. Remote State

Store state in a **shared backend** instead of local disk.

Common backends:

* AWS S3
* Azure Blob Storage
* GCS (Google Cloud Storage)
* Terraform Cloud

### Example: S3 backend

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/network/terraform.tfstate"
    region = "eu-central-1"

    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### Benefits:

* ✅ Shared across team
* ✅ Always up-to-date
* ✅ Versioning (if enabled on bucket)
* ✅ Better security

---

## 2. State Locking

Prevents **simultaneous modifications** to state.

### Why it matters:

Without locking:

```
Dev A → terraform apply
Dev B → terraform apply (same time)

💥 State corruption or race conditions
```

---

### How locking works (AWS example):

* Terraform creates a **lock entry** in DynamoDB
* Other users must wait until lock is released

```
Lock acquired → Apply runs → Lock released
```

---

### Locking backend examples:

| Backend         | Locking Mechanism        |
| --------------- | ------------------------ |
| S3              | DynamoDB                 |
| Terraform Cloud | Built-in                 |
| Azure Blob      | Native blob locking      |
| GCS             | Generation-based locking |

---

## 3. Remote State Data Sharing

You can also **read state from another Terraform project**:

```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket = "my-terraform-state"
    key    = "prod/vpc/terraform.tfstate"
    region = "eu-central-1"
  }
}
```

Then use outputs:

```hcl
data.terraform_remote_state.vpc.outputs.vpc_id
```

👉 Useful for:

* Microservices infra
* Shared VPC setups
* Modular architecture

---

# Commands

### Initialize backend

```bash
terraform init
```

If backend config changes:

```bash
terraform init -reconfigure
```

---

### Show current state

```bash
terraform show
```

---

### List resources in state

```bash
terraform state list
```

---

### Pull remote state locally

```bash
terraform state pull
```

---

### Push state (rare, dangerous)

```bash
terraform state push
```

---

### Force unlock (if stuck)

```bash
terraform force-unlock <LOCK_ID>
```

⚠️ Use only if you're sure no one else is running Terraform

---

# Gotchas

## 1. State contains secrets

* DB passwords
* API keys
* Private IPs

👉 Always:

* Enable encryption (e.g. `encrypt = true` in S3)
* Restrict access (IAM policies)

---

## 2. Locking is NOT optional in teams

If you use S3 without DynamoDB:

* ❌ No locking
* ❌ High risk of corruption

👉 Always configure locking

---

## 3. State file is NOT just cache

Many assume:

> “Terraform can just recreate state”

❌ Wrong

State contains:

* Resource IDs
* Dependencies
* Metadata

Losing it = losing control of infra

---

## 4. Manual edits are dangerous

```bash
vim terraform.tfstate ❌
```

👉 Instead use:

```bash
terraform state mv
terraform state rm
terraform import
```

---

## 5. Remote state ≠ remote execution

* Remote state → where state is stored
* Remote execution → where Terraform runs (e.g. Terraform Cloud)

👉 These are different concepts

---

## 6. Lock can get stuck

Example causes:

* Crashed `terraform apply`
* Network issues

Fix:

```bash
terraform force-unlock <id>
```

---

## 7. State drift still possible

Even with remote state:

```bash
aws console → manually change resource
```

Terraform won’t know until:

```bash
terraform plan
```