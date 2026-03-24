## Problem

In Kubernetes, containers share cluster resources (CPU, memory). Without constraints:

* One pod can **consume all node resources**, starving others
* Scheduling becomes unpredictable (pods placed on nodes that can’t actually handle them)
* Memory overuse can cause **OOM kills**
* CPU contention leads to **performance degradation**

You need a way to:

* Reserve resources (guarantee minimums)
* Cap usage (prevent noisy neighbors)

---

## Solution

Kubernetes provides **`requests`** and **`limits`** per container.

### 1. Requests (guaranteed minimum)

* Defines how much CPU/memory a container **needs**
* Used by the **scheduler** to decide placement
* Ensures the node has enough capacity

Example:

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "256Mi"
```

👉 Meaning:

* At least **0.5 CPU** and **256MB RAM** reserved

---

### 2. Limits (hard cap)

* Defines the **maximum** a container can use

```yaml
resources:
  limits:
    cpu: "1"
    memory: "512Mi"
```

👉 Meaning:

* CPU max: 1 core
* Memory max: 512MB

---

### 3. Runtime behavior

| Resource | If exceeding limit                  |
| -------- | ----------------------------------- |
| CPU      | Throttled (slower execution)        |
| Memory   | Container is **killed (OOMKilled)** |

---

### 4. QoS Classes (important!)

Kubernetes assigns QoS class based on requests/limits:

| QoS Class  | Condition          | Priority |
| ---------- | ------------------ | -------- |
| Guaranteed | requests == limits | Highest  |
| Burstable  | requests < limits  | Medium   |
| BestEffort | no requests/limits | Lowest   |

👉 Affects eviction when node is under pressure

---

## Commands

### Check pod resource usage

```bash
kubectl top pod
```

### Describe pod (see requests/limits)

```bash
kubectl describe pod <pod-name>
```

### View node capacity

```bash
kubectl describe node <node-name>
```

### Apply resource config

```bash
kubectl apply -f deployment.yaml
```

### Check why pod was killed

```bash
kubectl describe pod <pod-name>
```

Look for:

```
Reason: OOMKilled
```

---

## Gotchas

### 1. CPU ≠ Memory behavior

* CPU → **throttled**
* Memory → **killed**
  👉 Memory limits must be chosen carefully

---

### 2. Requests too high → scheduling issues

If requests exceed node capacity:

* Pod stays in **Pending**

---

### 3. Limits too low → unstable apps

* Frequent OOMKills
* GC-heavy apps (Java 👀) suffer badly

---

### 4. No limits = dangerous in shared clusters

* Pods can **eat all memory**
* Leads to node instability

---

### 5. Java apps need tuning

For JVM-based apps:

* Set:

  * `-Xmx` aligned with memory limit
* Otherwise:

  * JVM may exceed container limit → OOMKilled

---

### 6. Default behavior depends on namespace policies

Using:

* `LimitRange`
* `ResourceQuota`

👉 These may auto-assign defaults or reject pods

---

### 7. Burstable pods can be evicted

Even if under limit:

* Lower QoS → higher eviction risk under pressure

