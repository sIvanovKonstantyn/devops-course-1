## Problem

When managing infrastructure with Terraform, resources rarely exist in isolation. A database depends on a network, an app depends on the database, IAM roles must exist before services use them, etc.

The challenge is:

* **Understanding the order** in which Terraform creates, updates, or destroys resources
* Avoiding **race conditions** (e.g., app starts before DB is ready)
* Debugging unexpected behavior when Terraform applies changes in parallel

Without a clear model, infrastructure changes can become unpredictable.

---

## Solution

Terraform builds a **dependency graph (DAG — Directed Acyclic Graph)** to determine execution order.

### 🔹 How it works

Terraform analyzes your configuration and constructs a graph where:

* **Nodes** = resources, data sources, modules
* **Edges** = dependencies between them

It then:

1. **Sorts resources topologically**
2. Executes them in the correct order
3. Runs independent resources **in parallel**

---

### 🔹 Types of dependencies

#### 1. Implicit dependencies (most common)

Created automatically when you reference another resource:

```hcl
resource "aws_instance" "app" {
  subnet_id = aws_subnet.main.id
}
```

Here:

* `aws_instance.app` depends on `aws_subnet.main`
* Terraform infers this from the reference

---

#### 2. Explicit dependencies

Defined manually using `depends_on`:

```hcl
resource "aws_instance" "app" {
  depends_on = [aws_db_instance.main]
}
```

Use this when Terraform **cannot infer dependency**.

---

#### 3. Hidden dependencies

Sometimes dependencies exist but are not obvious in code:

* Provisioners
* External scripts
* Side effects (e.g., IAM policy propagation)

These require manual `depends_on`.

---

### 🔹 Execution behavior

* Terraform runs **parallel operations** where possible
* Default parallelism: **10 resources at once**
* Graph ensures:

  * Dependencies are respected
  * Maximum speed otherwise

---

### 🔹 Destroy graph

Terraform also builds a **reverse dependency graph** for destruction:

* If A depends on B → B is destroyed **after** A

---

## Commands

### Visualize the dependency graph

```bash
terraform graph
```

This outputs DOT format.

To render it visually using Graphviz:

```bash
terraform graph | dot -Tpng > graph.png
```

You can then open `graph.png`.

---

### Apply with controlled parallelism

```bash
terraform apply -parallelism=5
```

---

### Debug execution order

```bash
terraform plan
```

Look for:

* Resource ordering
* Dependencies inferred by Terraform

---

## Gotchas

### ⚠️ Overusing `depends_on`

* Makes graph more rigid
* Reduces parallelism
* Slows down execution

👉 Prefer implicit dependencies whenever possible

---

### ⚠️ Missing dependencies

Terraform **won’t detect**:

* API-level delays (e.g., IAM propagation in AWS)
* External scripts modifying resources

👉 Fix with `depends_on` or retries

---

### ⚠️ Data sources are part of the graph

Even read-only data sources:

```hcl
data "aws_ami" "latest" { ... }
```

* Can introduce dependencies
* May affect ordering

---

### ⚠️ Cyclic dependencies

Terraform will fail with:

```
Cycle: resource A → resource B → resource A
```

👉 You must break the cycle (e.g., split resources or refactor inputs)

---

### ⚠️ Graph ≠ execution logs

* Graph shows **possible execution order**
* Actual execution may vary due to parallelism