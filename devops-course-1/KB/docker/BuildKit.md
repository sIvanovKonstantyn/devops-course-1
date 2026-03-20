# Problem

Traditional Docker builds (the “classic builder”) have several limitations:

* Slow builds due to **sequential execution**
* Inefficient caching (all-or-nothing layer reuse)
* No advanced features like mounting secrets or caching dependencies properly
* Poor visibility into what’s happening during build

This becomes a bottleneck for modern apps (e.g., Node, Java, multi-stage builds).

---

# Solution

**BuildKit** is a **next-generation build engine for Docker** that improves performance, caching, and flexibility.

It replaces the legacy builder and introduces a smarter build system.

### Key improvements:

#### 1. Parallel builds

BuildKit can execute independent steps **in parallel**, instead of strictly top-to-bottom.

---

#### 2. Advanced caching

* More granular caching (not just full layers)
* Can reuse cache **across builds and environments**
* Supports **remote cache** (e.g., CI/CD pipelines)

---

#### 3. Mountable caches (huge for devs)

You can cache things like dependencies without baking them into layers:

```dockerfile
RUN --mount=type=cache,target=/root/.m2 mvn install
```

→ Perfect for:

* Maven / Gradle
* npm / yarn
* pip

---

#### 4. Secrets support (secure)

No more leaking secrets into image layers:

```dockerfile
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```

---

#### 5. Better output & debugging

More readable logs:

```bash
docker build --progress=plain .
```

---

#### 6. Smaller and cleaner images

BuildKit avoids unnecessary intermediate layers and can optimize output.

---

#### 7. Inline cache export/import

You can push cache to a registry and reuse it later:

```bash
docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t my-app .
```

---

# Commands

### Enable BuildKit (temporary)

```bash
DOCKER_BUILDKIT=1 docker build -t my-app .
```

---

### Enable BuildKit (permanently)

```bash
export DOCKER_BUILDKIT=1
```

Or in Docker config:

```json
{
  "features": {
    "buildkit": true
  }
}
```

---

### Use cache mount (example: npm)

```dockerfile
RUN --mount=type=cache,target=/root/.npm npm install
```

---

### Use secret during build

```bash
docker build --secret id=mysecret,src=secret.txt .
```

---

### Use plain logs

```bash
docker build --progress=plain .
```

---

# Gotchas

### 1. Syntax must be enabled for advanced features

To use mounts/secrets, add at top of Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1.4
```

---

### 2. Not all environments enable BuildKit by default

Older Docker versions or CI systems may still use the legacy builder.

---

### 3. Cache mounts are NOT image layers

Data in:

```dockerfile
--mount=type=cache
```

is **not persisted in the final image**.

→ Good for speed, but don’t expect files to exist later.

---

### 4. Secrets are ephemeral

Secrets are only available during the specific `RUN` command.

---

### 5. Debugging can feel different

Because of parallelism, logs may appear **out of order** compared to classic builds.

---

### 6. Requires newer Docker versions

Some features only work with newer Docker + BuildKit syntax versions.
