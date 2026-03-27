# 🧱 What is a Terraform Module?

A **module** in Terraform is simply a **container for resources** that are used together.

* The **root module** → your main working directory (where you run `terraform apply`)
* **Child modules** → reusable components you call from the root module (or other modules)

👉 Think of modules like **functions in programming**:

* Input → variables
* Output → values
* Internal logic → resources

---

## 📦 Example Without Modules (Bad Practice)

```hcl
resource "aws_instance" "app" {
  ami           = "ami-123"
  instance_type = "t2.micro"
}

resource "aws_security_group" "app_sg" {
  ...
}
```

👉 Problem:

* Hard to reuse
* Repetition across environments
* No abstraction

---

## ✅ Example With a Module

```hcl
module "app_server" {
  source = "./modules/ec2-instance"

  instance_type = "t2.micro"
  environment   = "dev"
}
```

Now your logic is reusable across:

* dev / staging / prod
* different projects

---

# 🧩 Module Structure (Standard Layout)

A well-designed module usually looks like this:

```
modules/
  ec2-instance/
    main.tf
    variables.tf
    outputs.tf
    README.md
```

---

## 🔹 main.tf

Defines resources

```hcl
resource "aws_instance" "this" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

---

## 🔹 variables.tf

Defines inputs

```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type"
}
```

---

## 🔹 outputs.tf

Exposes results

```hcl
output "instance_id" {
  value = aws_instance.this.id
}
```

---

# 🧠 How Terraform Modules Work (Flow)

1. Root module calls child module
2. Passes **input variables**
3. Module creates resources
4. Returns **outputs**

---

# 🏗️ How to Design Good Terraform Modules

This is where most people struggle. Let’s go deeper.

---

## 1. 🎯 Single Responsibility Principle

A module should do **one thing well**.

✅ Good:

* `vpc` module
* `ec2-instance` module
* `rds` module

❌ Bad:

* “infra-everything” module

---

## 2. 🔌 Use Inputs for Customization

Avoid hardcoding.

❌ Bad:

```hcl
instance_type = "t2.micro"
```

✅ Good:

```hcl
instance_type = var.instance_type
```

---

## 3. 📤 Expose Only Useful Outputs

Don’t expose everything.

✅ Good:

```hcl
output "public_ip" {
  value = aws_instance.this.public_ip
}
```

❌ Bad:

* dumping entire resource objects

---

## 4. 🧱 Composition Over Complexity

Instead of one huge module:

👉 Combine smaller modules:

```hcl
module "network" {
  source = "./modules/vpc"
}

module "app" {
  source = "./modules/ec2"
  vpc_id = module.network.vpc_id
}
```

---

## 5. 🧼 Keep Interfaces Clean

Your module should feel like an API.

Good module = easy to understand:

* minimal required inputs
* sensible defaults

---

## 6. ⚙️ Use Defaults Where Possible

```hcl
variable "instance_type" {
  default = "t3.micro"
}
```

👉 Makes module easier to use

---

## 7. 🔐 Avoid Provider Configuration Inside Modules

❌ Bad:

```hcl
provider "aws" {
  region = "us-east-1"
}
```

✅ Good:

* Define provider in root module
* Pass values via variables if needed

---

## 8. 📁 Support Multiple Environments

Use variables like:

```hcl
variable "environment" {}
```

Then tag resources:

```hcl
tags = {
  Environment = var.environment
}
```

---

## 9. 🧪 Make Modules Testable

* Use `terraform plan`
* Use tools like:

  * Terratest (Go)
  * Kitchen-Terraform

---

## 10. 📚 Document Everything

Your `README.md` should include:

* Inputs
* Outputs
* Example usage

---

# 🧠 Advanced Patterns

---

## 🔁 Module Reuse with for_each

```hcl
module "servers" {
  source = "./modules/ec2"

  for_each = toset(["dev", "staging", "prod"])

  environment = each.key
}
```

---

## 🧩 Nested Modules

Modules can call other modules:

```
app module
  ├── ec2 module
  ├── security group module
```

---

## 🌍 Remote Modules

You can use modules from:

* GitHub
* Terraform Registry

```hcl
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
}
```

---

# 🚨 Common Mistakes

❌ Over-engineering modules
❌ Too many variables
❌ Tight coupling between modules
❌ Breaking backward compatibility
❌ Hardcoding values

---

# 💡 Mental Model

Think of Terraform modules like:

| Concept     | Equivalent       |
| ----------- | ---------------- |
| Module      | Function / Class |
| Variables   | Parameters       |
| Outputs     | Return values    |
| Root module | Main program     |

---

# 🚀 Example: Real-World Design

**Goal:** Deploy a backend service

Structure:

```
modules/
  vpc/
  security-group/
  ec2/
  rds/

envs/
  dev/
  prod/
```

Then:

```hcl
module "vpc" { ... }

module "db" {
  source = "../../modules/rds"
  vpc_id = module.vpc.vpc_id
}

module "app" {
  source = "../../modules/ec2"
  db_host = module.db.endpoint
}
```

---

# 🧩 Final Takeaway

A good Terraform module is:

* 🔁 Reusable
* 🎯 Focused
* 🧼 Clean interface
* 🔧 Configurable
* 📦 Composable