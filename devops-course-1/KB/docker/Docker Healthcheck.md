# Problem

When running containers in production, it’s often insufficient to check if a container is merely **running**. A container might be up but its application inside could be failing (e.g., a web server not responding, a database in a bad state). Without proper monitoring, orchestrators like Docker Swarm or Kubernetes might keep sending traffic to an unhealthy container, causing downtime or errors.

---

# Solution

Docker provides the `HEALTHCHECK` instruction in a Dockerfile to define a command that tests the container’s health. Docker runs this command periodically, and the container gets one of three health statuses:

* `healthy` — the container is working as expected.
* `unhealthy` — the container failed the health check.
* `starting` — the health check has not yet passed for the first time.

This allows:

* Orchestrators to automatically restart unhealthy containers.
* Monitoring systems to track container health.
* Developers to detect issues inside a running container without manual intervention.

You can define a `HEALTHCHECK` in the Dockerfile or override it at runtime.

---

# Commands

**1. In Dockerfile**

```dockerfile
# Use an official image
FROM nginx:alpine

# Healthcheck every 30s, fail after 3 retries
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

**2. In `docker run`**

```bash
docker run -d --name mynginx \
  --health-cmd="curl -f http://localhost/ || exit 1" \
  --health-interval=30s \
  --health-retries=3 \
  nginx:alpine
```

**3. Check container health**

```bash
docker ps
docker inspect --format='{{json .State.Health}}' mynginx
```

**4. Reacting to health status**

```bash
docker events --filter 'container=mynginx'
# Or in orchestrators like Docker Swarm/K8s, containers can be auto-restarted
```

---

# Gotchas

* **Health check does not block container start** — a container can be `unhealthy` but still `running`.
* **Overly aggressive intervals** can increase load; choose reasonable `--interval` and `--timeout`.
* **Long startup times** — use `--start-period` to allow services to initialize before health checks begin.
* **`HEALTHCHECK NONE`** can disable inherited health checks from base images.
* **Non-zero exit codes** signal failure; returning `0` signals success.