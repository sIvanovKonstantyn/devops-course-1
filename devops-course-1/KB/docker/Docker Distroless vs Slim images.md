# Problem

Standard Docker images (like `ubuntu`, `node`, `openjdk`) are **bloated and insecure by default**:

* Include unnecessary tools (bash, package managers, curl, etc.)
* Larger image sizes → slower builds & deployments
* Bigger attack surface → more CVEs
* Not optimized for running a single production process

Example: a typical `node:18` image can be **~300MB+**, while your app might need only a fraction of that.

---

# Solution

## 1. Slim Images

Slim images (e.g. `node:18-slim`, `openjdk:17-slim`) are:

* Minimal OS (usually Debian stripped down)
* Still include package manager (`apt`)
* Still allow shell access

### Pros

* Smaller (30–70% reduction)
* Easier debugging (shell available)
* Compatible with most tools

### Cons

* Still includes unnecessary components
* Still some attack surface

---

## 2. Distroless Images

Distroless images (from Google) go further:

> They contain **ONLY your app + runtime dependencies**

No:

* shell
* package manager
* OS utilities

Examples:

* `gcr.io/distroless/java17`
* `gcr.io/distroless/nodejs`
* `gcr.io/distroless/base`

### Pros

* Extremely small
* Minimal attack surface
* More secure by design
* Production-focused

### Cons

* No shell → harder debugging
* Must build everything beforehand
* Requires multi-stage builds

---

# Commands

## Slim Example

```dockerfile
FROM node:18-slim

WORKDIR /app
COPY package*.json ./
RUN npm install --production

COPY . .
CMD ["node", "index.js"]
```

---

## Distroless Example (Multi-stage build)

```dockerfile
# Build stage
FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install --production

COPY . .

# Runtime stage (distroless)
FROM gcr.io/distroless/nodejs18

WORKDIR /app
COPY --from=builder /app .

CMD ["index.js"]
```

---

## Image Size Comparison

```bash
docker images
```

Typical results:

* node:18 → ~300MB
* node:18-slim → ~120MB
* distroless → ~50MB or less

---

# Gotchas

### 1. No Shell (Distroless)

You **cannot do this**:

```bash
docker exec -it container sh
```

Because:

* No `/bin/sh`
* No bash

👉 Debug using:

* Logs (`docker logs`)
* Temporary debug images
* Sidecar containers

---

### 2. You Must Build Everything Upfront

No package manager means:

❌ This won't work:

```dockerfile
RUN apt-get install curl
```

👉 Install everything in the **builder stage**

---

### 3. Harder Debugging

Slim:

* You can SSH / exec into container

Distroless:

* You can't inspect runtime easily

👉 Strategy:

* Use slim in dev
* Use distroless in prod

---

### 4. Compatibility Issues

Some apps assume:

* `/bin/bash`
* system libraries
* OS tools

Distroless may break them.

---

### 5. Logging Only via STDOUT

Since no tools exist:

* No `tail`, `less`, etc.

👉 Always log to:

```bash
stdout / stderr
```

---

# TL;DR

* **Slim** → smaller, still flexible, easier debugging
* **Distroless** → minimal, secure, production-grade

👉 Common pattern:

* Dev → slim
* Prod → distroless
