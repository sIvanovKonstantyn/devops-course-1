## Problem

In Kubernetes, understanding what happens to a Pod from creation to termination is critical for debugging, reliability, and designing resilient systems.

Many issues (crashes, restarts, stuck deployments) come from misunderstanding **Pod lifecycle states**, **container states**, and **how Kubernetes controllers react to them**.

---

## Solution

### 1. High-level Pod lifecycle phases

A Pod goes through these **phases**:

* **Pending**

  * Pod is created but not yet scheduled or containers not ready
  * Reasons:

    * No available node
    * Image is still downloading

* **Running**

  * Pod is scheduled to a node
  * At least one container is running or starting

* **Succeeded**

  * All containers finished successfully (exit code 0)
  * Typical for Jobs

* **Failed**

  * At least one container exited with failure (non-zero code)

* **Unknown**

  * Node communication lost (rare, usually node failure)

---

### 2. Container states inside a Pod

Each container has its own state:

* **Waiting**

  * Example reasons:

    * `ImagePullBackOff`
    * `CrashLoopBackOff`

* **Running**

  * Container is executing normally

* **Terminated**

  * Container stopped
  * Has:

    * exit code
    * reason
    * start/finish timestamps

---

### 3. Lifecycle flow (simplified)

```
Pod created
   ↓
Scheduler assigns node
   ↓
Kubelet pulls image
   ↓
Containers start (initContainers first)
   ↓
Pod becomes Running
   ↓
App runs
   ↓
Container exits OR Pod deleted
   ↓
Termination phase
```

---

### 4. Init containers

* Run **before main containers**
* Must complete successfully
* Common uses:

  * DB migrations
  * config setup

---

### 5. Probes (affect lifecycle behavior)

* **Liveness probe**

  * Fails → container restarted

* **Readiness probe**

  * Fails → removed from Service endpoints

* **Startup probe**

  * Protects slow-start apps

---

### 6. Termination lifecycle

When a Pod is deleted:

1. Kubernetes sends **SIGTERM**
2. Pod enters **Terminating**
3. Waits `terminationGracePeriodSeconds` (default 30s)
4. If still running → **SIGKILL**

Optional:

* **preStop hook** runs before SIGTERM completes

---

## Commands

### Check Pod status

```bash
kubectl get pods
```

### Detailed lifecycle info

```bash
kubectl describe pod <pod-name>
```

### Watch state changes live

```bash
kubectl get pods -w
```

### Inspect container state

```bash
kubectl get pod <pod-name> -o jsonpath="{.status.containerStatuses[*].state}"
```

### Check logs (important for crashes)

```bash
kubectl logs <pod-name>
```

### Previous crash logs

```bash
kubectl logs <pod-name> --previous
```

---

## Gotchas

### 1. Pod ≠ container

A Pod can have multiple containers → lifecycle confusion happens here.

---

### 2. `Running` does NOT mean healthy

* Pod can be Running but:

  * app is broken
  * readiness probe failing
    👉 traffic won’t reach it

---

### 3. CrashLoopBackOff trap

* Happens when:

  * app starts → crashes → restarts repeatedly
* Kubernetes adds **backoff delay**

---

### 4. Deleting Pod is not instant

* Respect `terminationGracePeriodSeconds`
* Can appear stuck in *Terminating*

---

### 5. Init containers block everything

* If one fails → Pod never reaches Running

---

### 6. Node issues = `Unknown` state

* Usually means:

  * node crashed
  * kubelet stopped

---

### 7. Jobs vs Deployments behavior

* **Job** → expects `Succeeded`
* **Deployment** → restarts Pods forever