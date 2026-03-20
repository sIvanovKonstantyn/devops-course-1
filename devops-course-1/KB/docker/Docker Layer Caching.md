# Problem

When building Docker images, every build can be **slow and inefficient** if all steps are executed from scratch each time. This becomes especially painful when:

* Installing dependencies repeatedly
* Rebuilding unchanged parts of the image
* Working with large projects

Without caching, even a tiny code change can trigger a **full rebuild**, wasting time and resources.

---

# Solution

Docker uses a **layer-based caching system** to speed up builds.

Each instruction in a `Dockerfile` (e.g., `FROM`, `RUN`, `COPY`) creates a **layer**. Docker caches these layers and reuses them if nothing has changed.

### How it works:

* Docker builds the image **step by step**
* For each instruction, it checks:

  * Has this exact instruction been run before?
  * Have the inputs (files, env, context) changed?
* If nothing changed → **reuse cached layer**
* If something changed → **invalidate this layer and all following layers**

### Key idea:

> Once a layer changes, all layers after it must be rebuilt.

---

# Commands

### Build with cache (default)

```bash
docker build -t my-app .
```

### Disable cache

```bash
docker build --no-cache -t my-app .
```

### Show build progress clearly

```bash
docker build --progress=plain -t my-app .
```

### Use BuildKit (better caching)

```bash
DOCKER_BUILDKIT=1 docker build -t my-app .
```

### Example optimized Dockerfile

```dockerfile
FROM node:18

# 1. Install dependencies first (cached)
COPY package.json package-lock.json ./
RUN npm install

# 2. Copy source code (changes often)
COPY . .

CMD ["npm", "start"]
```

---

# Gotchas

### 1. Order matters (a lot)

Bad:

```dockerfile
COPY . .
RUN npm install
```

→ Any code change invalidates `npm install`

Good:

```dockerfile
COPY package*.json ./
RUN npm install
COPY . .
```

---

### 2. COPY invalidates cache easily

Even changing **one file** in the copied directory breaks the cache for that layer.

Use `.dockerignore` to avoid unnecessary invalidation:

```
node_modules
.git
*.log
```

---

### 3. RUN commands are cache-sensitive

This:

```dockerfile
RUN apt-get update && apt-get install -y curl
```

is cached forever unless something before it changes.

→ You might get **outdated packages** unintentionally.

---

### 4. Cache is based on instruction + context

Even whitespace or environment changes can break cache:

```dockerfile
RUN echo "hello"
```

Changing to:

```dockerfile
RUN echo "hello world"
```

→ invalidates layer

---

### 5. Multi-stage builds help caching

You can isolate heavy steps (like build tools) so they don’t affect the final image cache.

---

### 6. BuildKit improves caching significantly

With BuildKit, you get:

* Better parallelism
* Advanced cache reuse
* Inline cache export/import