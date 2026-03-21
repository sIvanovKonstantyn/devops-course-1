## Problem

When building Docker images, you often face a trade-off:

* You need **large images** with build tools (compilers, Maven, Node, etc.) to compile your app
* But you want **small, secure runtime images** in production

If you use a single-stage build:

* Your final image includes **everything** (build tools + source code + dependencies)
* This leads to:

  * ❌ Large image size
  * ❌ Slower deployments
  * ❌ Bigger attack surface

---

## Solution

**Multi-stage builds** let you use multiple `FROM` statements in one Dockerfile and **copy only what you need** into the final image.

### Core idea:

1. Use a **builder stage** (heavy image with tools)
2. Compile/build your app
3. Copy the result into a **lightweight runtime stage**

---

### Example (Java with Maven)

```dockerfile
# Stage 1: Build
FROM maven:3.9.6-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:17-jdk-jammy
WORKDIR /app
COPY --from=builder /app/target/app.jar app.jar

CMD ["java", "-jar", "app.jar"]
```

### What happens:

* First stage builds the JAR
* Second stage copies only the JAR → no Maven, no source code

---

### Result:

* ✅ Smaller image (often 5–10x smaller)
* ✅ Cleaner runtime
* ✅ Better security

---

## Commands

### Build image

```bash
docker build -t my-app .
```

### Run container

```bash
docker run -p 8080:8080 my-app
```

---

### Build a specific stage (for debugging)

```bash
docker build --target builder -t my-app-builder .
```

---

### Inspect image size

```bash
docker images
```

---

## Gotchas

### 1. Cache invalidation

Docker caches layers aggressively.

❗ If you do:

```dockerfile
COPY . .
RUN mvn package
```

Any file change invalidates the whole build.

✅ Better:

```dockerfile
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package
```

---

### 2. File paths between stages

You must copy from the correct path:

```dockerfile
COPY --from=builder /app/target/app.jar app.jar
```

If the path is wrong → build fails silently or copies nothing.

---

### 3. Naming stages

Always name stages:

```dockerfile
FROM node:18 AS builder
```

Otherwise you’ll rely on numeric indexes:

```dockerfile
COPY --from=0 ...
```

❌ Hard to maintain

---

### 4. Missing runtime dependencies

Your app might work in builder stage but fail in runtime stage because:

* Native libs missing
* OS packages missing

Example:

```dockerfile
RUN apt-get update && apt-get install -y libssl-dev
```

---

### 5. Over-optimizing base images

Using ultra-minimal images like `alpine` can cause:

* glibc vs musl issues
* unexpected runtime bugs

---

### 6. Secrets leakage

If you copy everything:

```dockerfile
COPY . .
```

You might accidentally include:

* `.env`
* private keys
* credentials

Use `.dockerignore`!