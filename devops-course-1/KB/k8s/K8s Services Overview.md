# Problem

In Kubernetes, Pods are **ephemeral**:

* They can restart, die, or be rescheduled
* Their IP addresses change constantly

So you can’t reliably connect to a Pod directly.

You need:

* A **stable endpoint**
* **Service discovery**
* **Load balancing** across Pods

---

# Solution

Kubernetes provides **Services** as an abstraction layer over Pods.

A Service:

* Selects Pods via labels
* Exposes them via a stable IP/DNS
* Optionally exposes them outside the cluster

There are 3 main types:

---

## 1. ClusterIP (default)

**What it is:**

* Internal-only Service
* Accessible **only inside the cluster**

**How it works:**

* Gets a virtual IP (ClusterIP)
* Traffic is load-balanced to matching Pods

**Use case:**

* Microservices talking to each other
* Backend APIs, databases, internal services

**Example:**

```
Frontend → Backend (ClusterIP)
```

---

## 2. NodePort

**What it is:**

* Exposes Service on each Node’s IP + static port

**How it works:**

* Kubernetes opens a port (30000–32767) on every node
* Traffic to:

  ```
  <NodeIP>:<NodePort>
  ```

  is forwarded to the Service → Pods

**Use case:**

* Quick external access (dev/test)
* When you don’t have a cloud load balancer

**Example:**

```
http://192.168.1.10:30007 → Service → Pods
```

---

## 3. LoadBalancer

**What it is:**

* Exposes Service externally using a cloud provider LB

**How it works:**

* Creates an external load balancer (AWS, GCP, Azure)
* Assigns a public IP
* Routes traffic → NodePort → Pods

**Use case:**

* Production external APIs
* Public-facing services

**Important:**

* Requires cloud provider integration

**Example:**

```
Internet → Cloud LB → Node → Pods
```

---

# Commands

### Create a deployment (example app)

```bash
kubectl create deployment nginx --image=nginx
```

---

### Expose as ClusterIP

```bash
kubectl expose deployment nginx \
  --port=80 \
  --target-port=80 \
  --type=ClusterIP
```

---

### Expose as NodePort

```bash
kubectl expose deployment nginx \
  --port=80 \
  --target-port=80 \
  --type=NodePort
```

Check assigned port:

```bash
kubectl get svc nginx
```

---

### Expose as LoadBalancer

```bash
kubectl expose deployment nginx \
  --port=80 \
  --target-port=80 \
  --type=LoadBalancer
```

Get external IP:

```bash
kubectl get svc nginx
```

---

### Access inside cluster (ClusterIP)

```bash
kubectl exec -it <pod> -- curl http://nginx
```

---

# Gotchas

### 1. NodePort is NOT secure by default

* Opens port on every node
* No auth, no TLS unless you add it

---

### 2. LoadBalancer depends on environment

* Works in:

  * AWS / GCP / Azure
* Doesn’t work natively in:

  * Minikube
  * Kind

👉 For local:

```bash
minikube service nginx
```

---

### 3. ClusterIP is NOT reachable externally

* Beginners often try:

  ```
  curl <ClusterIP>
  ```

  from outside → won’t work

---

### 4. NodePort still uses ClusterIP internally

* Flow:

  ```
  NodePort → ClusterIP → Pods
  ```
* It’s layered, not separate

---

### 5. No built-in path-based routing

* Services do **L4 routing only (TCP/UDP)**
* For:

  * `/api`
  * `/auth`

👉 You need:

* Ingress + Ingress Controller

---

### 6. Health checks are NOT automatic

* Service doesn’t know if Pod is “healthy”
* You must configure:

  * readinessProbe
  * livenessProbe