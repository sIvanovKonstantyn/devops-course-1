# Problem

Applications need configuration (API URLs, feature flags, credentials, etc.), but:

* Hardcoding config into code = ❌ inflexible, requires rebuild/redeploy
* Using environment-specific builds = ❌ messy and error-prone
* Storing secrets in plain text (Git, images) = ❌ security risk

You need a way to:

* Inject config dynamically at runtime
* Separate config from application code
* Handle **sensitive vs non-sensitive data differently**

---

# Solution

Kubernetes provides two resources:

## 1. ConfigMap

Used for **non-sensitive configuration**

Examples:

* App settings (`LOG_LEVEL=debug`)
* URLs (`API_BASE=https://api.example.com`)
* Feature flags

How it works:

* Stores key-value pairs
* Can be injected into Pods as:

  * Environment variables
  * Files (mounted volumes)

---

## 2. Secret

Used for **sensitive data**

Examples:

* Passwords
* API keys
* Tokens
* TLS certificates

How it works:

* Similar to ConfigMap, but:

  * Values are **base64-encoded**
  * Stored separately with stricter access controls
* Can also be injected as env vars or files

⚠️ Important: base64 ≠ encryption (just encoding)

---

## Key Difference

| Feature   | ConfigMap          | Secret                  |
| --------- | ------------------ | ----------------------- |
| Purpose   | Non-sensitive data | Sensitive data          |
| Encoding  | Plain text         | Base64                  |
| Security  | Low                | Higher (RBAC, policies) |
| Use cases | Config             | Credentials             |

---

# Commands

## Create ConfigMap

```bash
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=debug \
  --from-literal=API_URL=https://api.example.com
```

From file:

```bash
kubectl create configmap app-config --from-file=config.properties
```

---

## Create Secret

```bash
kubectl create secret generic app-secret \
  --from-literal=DB_PASSWORD=mysecret \
  --from-literal=API_KEY=123456
```

From file:

```bash
kubectl create secret generic app-secret --from-file=secrets.env
```

---

## Use in Pod (env vars)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
    - name: app
      image: my-app
      env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: DB_PASSWORD
```

---

## Use as Volume

```yaml
volumeMounts:
  - name: config-volume
    mountPath: /etc/config

volumes:
  - name: config-volume
    configMap:
      name: app-config
```

---

## Inspect

```bash
kubectl get configmap app-config -o yaml
kubectl get secret app-secret -o yaml
```

---

# Gotchas

### 1. Secrets are NOT really secure by default

* Base64 is easily decoded:

  ```bash
  echo "bXlzZWNyZXQ=" | base64 -d
  ```
* Use:

  * RBAC
  * Encryption at rest
  * External secret managers (Vault, AWS Secrets Manager)

---

### 2. Updates are NOT always instant

* Env vars → require pod restart ❗
* Mounted volumes → auto-update (with delay)

---

### 3. Size limits

* Max size per object: ~1MB
* Don’t store large files

---

### 4. ConfigMap/Secret = not versioned

* Changes overwrite existing data
* No built-in rollback

👉 Common pattern:

* Use immutable names (`app-config-v2`)
* Or use Helm versioning

---

### 5. Accidental leaks

* `kubectl get secret -o yaml` exposes values (base64)
* Logs / debug prints can leak secrets

---

### 6. File vs Env usage tradeoff

| Method   | Pros            | Cons                  |
| -------- | --------------- | --------------------- |
| Env vars | Simple          | Requires restart      |
| Volumes  | Dynamic updates | Slightly more complex |
