## # Problem

In Kubernetes, you typically define a fixed number of pod replicas for your application. That creates a mismatch with real-world traffic:

* Traffic is **dynamic** (spikes, drops, daily patterns)
* Resources are **finite and costly**
* Manual scaling is **slow and error-prone**

Common issues:

* 🚨 Under-scaling → high latency, timeouts, crashes
* 💸 Over-scaling → wasted CPU/memory, higher cloud costs
* 🧠 Manual intervention → not viable in production systems

You need a way to automatically adjust the number of pods based on load.

---

## # Solution

Kubernetes provides **Horizontal Pod Autoscaler (HPA)** to solve this.

**What it does:**

* Automatically scales the number of pod replicas in a Deployment/ReplicaSet
* Uses metrics like:

  * CPU utilization (default)
  * Memory usage
  * Custom metrics (e.g. requests/sec, queue size)

**How it works (simplified):**

1. HPA periodically fetches metrics from **Metrics Server**
2. Compares current metric vs target (e.g. CPU 70%)
3. Adjusts replicas proportionally

Formula (conceptual):

```
desiredReplicas = currentReplicas * (currentMetric / targetMetric)
```

**Example:**

* Target CPU: 70%
* Current CPU: 140%
  → Scale from 2 pods → 4 pods

**Key components:**

* HPA controller (in control plane)
* Metrics Server (cluster addon)
* Resource requests/limits (important for correct scaling)

---

## # Commands

### 1. Install Metrics Server (required)

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

---

### 2. Create HPA

**Autoscale a Deployment:**

```
kubectl autoscale deployment my-app \
  --cpu-percent=70 \
  --min=2 \
  --max=10
```

---

### 3. YAML-based HPA (recommended)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Apply:

```
kubectl apply -f hpa.yaml
```

---

### 4. Check HPA status

```
kubectl get hpa
kubectl describe hpa my-app-hpa
```

---

### 5. Load testing (to trigger scaling)

```
kubectl run -i --tty load-generator --rm --image=busybox -- /bin/sh
```

Inside:

```
while true; do wget -q -O- http://my-app; done
```

---

## # Gotchas

### 1. ⚠️ Metrics Server is mandatory

Without it, HPA shows:

```
unable to get metrics for resource cpu
```

---

### 2. ❗ Resource requests must be set

HPA uses **% of requested CPU**, not actual CPU.

Bad:

```yaml
resources: {}
```

Good:

```yaml
resources:
  requests:
    cpu: 200m
```

If missing → scaling behaves incorrectly or not at all.

---

### 3. 🐢 Scaling is not instant

* Default sync period ~15s
* Cooldowns prevent flapping
* Expect delays (30–60s+)

---

### 4. 📉 Scale down is conservative

K8s avoids aggressive downscaling to prevent:

* traffic spikes
* cold starts

---

### 5. 🧮 CPU ≠ real load (sometimes)

CPU is a **poor proxy** for:

* I/O-bound apps
* queue-based systems

👉 Use **custom metrics** (Prometheus Adapter) when needed

---

### 6. 🔄 HPA + Cluster Autoscaler

HPA adds pods, but:

* If cluster has no free nodes → pods stay Pending

You need:

* HPA → scale pods
* Cluster Autoscaler → scale nodes

---

### 7. 📦 Stateful apps need care

HPA works best with:

* stateless services

For stateful workloads:

* scaling may break consistency or performance

