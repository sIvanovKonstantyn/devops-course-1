## 🧩 Problem

When you run applications in Docker containers, they are isolated by default—including their network stack.

This creates several challenges:

* Containers can’t automatically talk to each other
* Exposing services (e.g., API, DB) to your host or the internet requires configuration
* Service discovery (how one container finds another) is not obvious
* Different environments (dev, staging, prod) need consistent networking

Without understanding Docker networking, you’ll run into issues like:

* “Why can’t my backend reach my database?”
* “Why is my app not accessible on localhost?”

---

## ✅ Solution

Docker solves this with **network drivers** and **virtual networks** that control how containers communicate.

### 1. Bridge Network (default)

* Used when you run `docker run` without specifying a network
* Containers get private IPs (e.g., `172.x.x.x`)
* Containers **can talk via IP**, but not by name (unless using custom bridge)

👉 Best for: simple, standalone containers

---

### 2. User-defined Bridge Network (most important)

* Custom network you create manually
* Built-in **DNS resolution** → containers can talk by name

```text
backend → http://db:5432
```

👉 Best for: multi-container apps (e.g., backend + DB)

---

### 3. Host Network

* Container shares host’s network stack
* No isolation, no port mapping needed

👉 Best for: high-performance or low-latency cases

---

### 4. None Network

* Completely disables networking

👉 Best for: security / offline jobs

---

### 5. Overlay Network

* Used in **Docker Swarm** (multi-host)
* Containers on different machines communicate

👉 Best for: distributed systems

---

### Key Concepts

**Port Mapping**

* Exposes container ports to host

```text
host:container
```

**DNS-based Service Discovery**

* Works automatically in user-defined networks
* Use container names instead of IPs

**Isolation**

* Containers only see others in the same network

---

## 💻 Commands

### Create a network

```bash
docker network create my-network
```

### Run containers in the same network

```bash
docker run -d --name db --network my-network postgres
docker run -d --name backend --network my-network my-app
```

### Access service by name

```bash
# inside backend container
curl http://db:5432
```

---

### Port mapping (expose to host)

```bash
docker run -p 8080:80 nginx
```

👉 Access via:

```
http://localhost:8080
```

---

### List networks

```bash
docker network ls
```

### Inspect network

```bash
docker network inspect my-network
```

---

### Connect running container to network

```bash
docker network connect my-network my-container
```

---

## ⚠️ Gotchas

### 1. ❌ “localhost” confusion

Inside a container:

* `localhost` = **the container itself**, NOT your host

Use:

* `host.docker.internal` (on Mac/Windows)
* or host IP on Linux

---

### 2. ❌ Default bridge has no DNS

Containers can’t resolve names unless you use a **user-defined network**

👉 Always prefer:

```bash
docker network create ...
```

---

### 3. ❌ Port mapping is only for host access

Containers in the same network **do NOT need `-p`**

Wrong mental model:

```text
backend → localhost:5432 ❌
```

Correct:

```text
backend → db:5432 ✅
```

---

### 4. ❌ Hardcoding IPs

Container IPs change frequently

👉 Always use container names

---

### 5. ❌ Multiple networks = isolation

If containers are on different networks, they **cannot see each other**

---

### 6. ⚠️ Host network removes isolation

Using `--network host`:

* No port conflicts protection
* Less secure