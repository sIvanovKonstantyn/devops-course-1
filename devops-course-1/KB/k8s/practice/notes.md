# 🚀 Kubernetes Practice Notes (Minikube, App on Port 5000)

---

# 🧱 0. Setup

Install:

* [Minikube](https://minikube.sigs.k8s.io/docs/start/?utm_source=chatgpt.com)
* [kubectl](https://kubernetes.io/docs/tasks/tools/?utm_source=chatgpt.com)
* [Docker](https://www.docker.com/?utm_source=chatgpt.com)

Start cluster:

```bash
minikube start
```

Enable addons:

```bash
minikube addons enable ingress
minikube addons enable metrics-server
```

---

# 🐳 1. Build Image (inside Minikube)

```bash
minikube image build -t my-app:1.0 .
```

Verify:

```bash
minikube image ls | grep my-app
```

---

# 📦 2. Deployment (App runs on 5000)

### `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:1.0
          imagePullPolicy: Never
          ports:
            - containerPort: 5000
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
```

Apply:

```bash
kubectl apply -f deployment.yaml
```

---

# 🔍 3. Verify Pods

```bash
kubectl get pods
```

If issues:

```bash
kubectl describe pod <pod>
kubectl logs <pod>
```

---

# 🌐 4. Service (Expose Port 5000)

### `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - port: 5000
      targetPort: 5000
  type: ClusterIP
```

Apply:

```bash
kubectl apply -f service.yaml
```

---

# 🧪 5. Test via Port Forward (CRITICAL STEP)

```bash
kubectl port-forward svc/my-app-service 8080:5000
```

Open:

```
http://localhost:8080
```

👉 If this fails → fix app or service BEFORE moving on

---

# 🌍 6. Ingress

### `ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
spec:
  rules:
    - host: my-app.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 5000
```

Apply:

```bash
kubectl apply -f ingress.yaml
```

---

# 🌐 7. Configure Local DNS

```bash
minikube ip
```

Edit `/etc/hosts`:

```
<MINIKUBE_IP> my-app.local
```

---

# 🧪 8. Test Ingress

```
http://my-app.local
```

---

# 🔐 9. Add TLS

## Generate cert

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=my-app.local/O=my-app"
```

---

## Create secret

```bash
kubectl create secret tls my-app-tls \
  --key tls.key \
  --cert tls.crt
```

---

## Update ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
spec:
  tls:
    - hosts:
        - my-app.local
      secretName: my-app-tls
  rules:
    - host: my-app.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 5000
```

Apply:

```bash
kubectl apply -f ingress.yaml
```

---

## Test HTTPS

```
https://my-app.local
```

⚠️ Self-signed warning is expected

---

# 📈 10. Autoscaling

```bash
kubectl autoscale deployment my-app \
  --cpu-percent=50 \
  --min=2 \
  --max=5
```

---

## Verify

```bash
kubectl get hpa
```

---

## Load test

```bash
kubectl run -i --tty load-generator --rm --image=busybox -- /bin/sh
```

Inside:

```sh
while true; do wget -q -O- http://my-app-service:5000; done
```

---

## Watch scaling

```bash
kubectl get pods -w
```

---

# 🧠 Key Takeaways

* Always align ports:

  ```
  containerPort = targetPort = app port (5000)
  ```
* `port-forward` is your first debugging tool
* Ingress requires host mapping
* TLS requires secret
* HPA requires metrics-server

---

# ⚡ Pro Tip

If something doesn’t work, ALWAYS run:

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl get endpoints
```
