# Problem

By default, Docker containers often run as **root**, which creates serious security risks:

* If an attacker escapes the container, they may gain **root access to the host**
* Images may contain **known vulnerabilities** (outdated packages, insecure libraries)
* Many developers push images to production **without scanning them**

This leads to:

* Privilege escalation risks
* Supply chain vulnerabilities
* Compliance issues (especially in regulated environments)

---

# Solution

## 1. Run containers as non-root

Instead of running as root, define a **non-root user inside the container**.

### Why it matters:

* Limits damage if the container is compromised
* Prevents direct root-level access to the host
* Follows the principle of least privilege

---

## 2. Scan images for vulnerabilities

Before deploying, scan Docker images for:

* Known CVEs
* Outdated dependencies
* Misconfigurations

### Common tools:

* Trivy (lightweight, very popular)
* Docker Scout (built into Docker)
* Snyk

---

## 3. Use minimal base images

* Prefer `alpine`, `distroless`, or slim variants
* Smaller images = smaller attack surface

---

## 4. Drop unnecessary privileges

Even non-root containers may have extra Linux capabilities.

Use:

* `--cap-drop`
* `--read-only`
* seccomp / AppArmor profiles

---

# Commands

## Run container as non-root

### Dockerfile example

```dockerfile
FROM node:18-alpine

# Create user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Switch to non-root
USER appuser

WORKDIR /app
COPY . .

CMD ["node", "app.js"]
```

---

## Run with explicit user

```bash
docker run --user 1000:1000 my-app
```

---

## Scan image with Trivy

```bash
trivy image my-app:latest
```

---

## Scan with Docker Scout

```bash
docker scout quickview my-app
```

---

## Drop capabilities

```bash
docker run \
  --cap-drop ALL \
  --read-only \
  --security-opt no-new-privileges \
  my-app
```

---

# Gotchas

### 1. File permissions break easily

* Non-root users may not access files copied into the image
* Fix with:

```dockerfile
RUN chown -R appuser:appgroup /app
```

---

### 2. Some apps expect root

* Binding to ports <1024 requires root
* Workaround: use higher ports (e.g., 3000, 8080)

---

### 3. Alpine can cause compatibility issues

* Some binaries expect `glibc`, but Alpine uses `musl`
* Consider `debian-slim` if you hit weird runtime errors

---

### 4. Scanners produce noise

* Not all vulnerabilities are exploitable
* Prioritize:

  * HIGH / CRITICAL
  * Runtime-relevant packages

---

### 5. “Non-root” ≠ fully secure

* You still need:

  * Network isolation
  * Secrets management
  * Runtime monitoring ,