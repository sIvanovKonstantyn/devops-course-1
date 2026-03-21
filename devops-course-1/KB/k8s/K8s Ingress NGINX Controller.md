## # Problem

In Kubernetes, exposing your application to the outside world is not straightforward.

* **Pods are ephemeral** → their IPs change constantly
* **Services** (ClusterIP) are internal-only by default
* **NodePort / LoadBalancer**:

  * expose each service separately
  * not flexible for routing (e.g., `/api` vs `/web`)
  * can become expensive (multiple cloud load balancers)

👉 The core problem:

> How do you expose multiple services over HTTP/HTTPS using a **single entry point with smart routing**?

---

## # Solution

Use **Ingress + Ingress Controller**

### 1. What is Ingress?

An **Ingress** is a Kubernetes resource that defines **HTTP/HTTPS routing rules**.

Example:

* `example.com/api` → backend service A
* `example.com/web` → backend service B

It does **not** handle traffic by itself.

---

### 2. What is NGINX Ingress Controller?

The NGINX Ingress Controller is a pod that:

* watches Ingress resources via Kubernetes API
* dynamically configures NGINX
* acts as a **reverse proxy + load balancer**

👉 Think of it as:

```
Internet → NGINX Ingress Controller → Kubernetes Services → Pods
```

---

### 3. How routing works

Example flow:

1. Request comes to:

   ```
   http://myapp.com/api/users
   ```
2. NGINX Ingress matches rule:

   ```
   /api → service-api
   ```
3. Forwards request to:

   ```
   Service → Pod
   ```

---

## # Commands

### 1. Install NGINX Ingress Controller

Using Helm:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install nginx-ingress ingress-nginx/ingress-nginx \
  --set controller.publishService.enabled=true
```

---

### 2. Example Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

---

### 3. Create Ingress Resource

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

---

### 4. Get external IP

```bash
kubectl get svc -n default
kubectl get ingress
```

---

### 5. Test locally

```bash
echo "<INGRESS_IP> myapp.local" | sudo tee -a /etc/hosts
curl http://myapp.local/api
```

---

## # Gotchas

### 1. Ingress does nothing without controller

Creating an Ingress resource alone:

```
❌ No traffic routing
```

You **must** install an Ingress Controller.

---

### 2. ingressClassName mismatch

If you forget:

```yaml
ingressClassName: nginx
```

👉 Your Ingress might be ignored.

---

### 3. Path matching quirks

* `Prefix` vs `Exact` matters
* `/api` ≠ `/api/` in some cases

👉 Can lead to unexpected routing bugs

---

### 4. TLS requires extra setup

You need:

* TLS secret
* cert manager (optional but recommended)

Example:

```yaml
tls:
  - hosts:
      - myapp.local
    secretName: my-tls-secret
```

---

### 5. Annotations = hidden complexity

NGINX behavior is often controlled via annotations:

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
```

👉 These are:

* powerful
* but non-obvious
* controller-specific

---

### 6. Debugging is not obvious

Useful commands:

```bash
kubectl describe ingress my-ingress
kubectl logs <nginx-ingress-pod>
kubectl get events
```

---

### 7. Single point of failure (if misconfigured)

* One Ingress Controller = one entry point
* If it goes down → everything is down

👉 Run multiple replicas + use a Service (LoadBalancer)