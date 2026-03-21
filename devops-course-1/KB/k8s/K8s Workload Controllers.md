# Problem

When running applications in Kubernetes, you need to answer:

* How many instances (pods) should run?
* How are they updated?
* Do they need stable identity or storage?
* Should they run on every node?

Different workloads have different requirements:

* Stateless APIs scale freely
* Databases need stable identity + storage
* Node-level agents must run everywhere

Using the wrong controller leads to:

* Data loss (e.g., DB in Deployment)
* Broken scaling
* Networking issues
* Painful updates

---

# Solution

## 1. Deployment (Stateless workloads)

**Use when:**

* App is stateless
* Any pod can serve any request
* Easy horizontal scaling

**What it does:**

* Manages ReplicaSets → Pods
* Supports rolling updates & rollbacks
* Pods are interchangeable

**Examples:**

* REST APIs
* Frontends
* Microservices

**Key properties:**

* Pods have random names
* No stable identity
* No guaranteed order

---

## 2. StatefulSet (Stateful workloads)

**Use when:**

* Each pod needs a stable identity
* Persistent storage per pod
* Ordered startup/shutdown matters

**What it does:**

* Gives each pod:

  * Stable name (`pod-0`, `pod-1`)
  * Stable DNS
  * Dedicated volume
* Controls deployment order

**Examples:**

* Databases (Postgres, MongoDB)
* Kafka, Zookeeper
* Redis cluster

**Key properties:**

* Pods are NOT interchangeable
* Storage sticks to pod identity
* Ordered scaling (0 → 1 → 2)

---

## 3. DaemonSet (Node-level workloads)

**Use when:**

* You need exactly one pod per node

**What it does:**

* Automatically runs a pod on every node
* New node → pod automatically scheduled

**Examples:**

* Logging agents (Fluentd)
* Monitoring (Prometheus Node Exporter)
* Security agents

**Key properties:**

* 1 pod per node (by default)
* Not used for scaling apps
* Tied to cluster infrastructure

---

# Commands

### Deployment

```bash
kubectl create deployment my-app --image=nginx
kubectl scale deployment my-app --replicas=5
kubectl rollout restart deployment my-app
kubectl rollout undo deployment my-app
```

---

### StatefulSet

```bash
kubectl apply -f statefulset.yaml
kubectl get pods -l app=my-db
kubectl delete pod my-db-0  # will be recreated with same identity
```

---

### DaemonSet

```bash
kubectl apply -f daemonset.yaml
kubectl get daemonsets
kubectl describe daemonset my-daemon
```

---

# Gotchas

## Deployment pitfalls

* ❌ Don’t use for databases → pods can be rescheduled anywhere
* ❌ Local storage is lost on restart
* ⚠️ Scaling too fast can overload downstream systems

---

## StatefulSet pitfalls

* ❌ Requires **Headless Service** (`clusterIP: None`)
* ❌ Deleting PVCs incorrectly = data loss
* ⚠️ Scaling down does NOT delete volumes automatically
* ⚠️ Slower rollout due to ordering

---

## DaemonSet pitfalls

* ❌ Runs on *every node* → resource usage explodes
* ⚠️ Needs tolerations for control-plane nodes
* ⚠️ Not meant for user-facing apps

---

## General mistakes

* Mixing stateless + stateful concerns
* Ignoring storage class behavior
* Not understanding pod identity vs replica count