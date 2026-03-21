# 🐳 Docker DevOps Practice: Backend + Frontend (Optimized Setup)

## 📌 Goal

Build a simple full-stack app:

* **Backend**: Python (Hello World API)
* **Frontend**: Static page served via Nginx, calling backend
* Use:

  * Multi-stage builds
  * Slim / distroless images
  * Non-root users
  * Docker Compose
  * Custom network
  * BuildKit

---

# 📁 Project Structure

```
project/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   └── Dockerfile
│
└── docker-compose.yml
```

---

# ⚙️ Step 1: Backend (Python API)

## `backend/app.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {"message": "Hello from backend"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## `backend/requirements.txt`

```
flask==3.0.0
```

---

# 🐍 Step 2: Optimized Backend Dockerfile

## Key ideas:

* Multi-stage build
* Use `python:slim`
* Run as non-root

## `backend/Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1.6

# ---- Builder stage ----
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Runtime stage ----
FROM python:3.11-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy installed packages
COPY --from=builder /root/.local /home/appuser/.local

# Copy app
COPY app.py .

# Set permissions
RUN chown -R appuser:appuser /app /home/appuser

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# 🌐 Step 3: Frontend (Static Page)

## `frontend/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Frontend</title>
</head>
<body>
    <h1>Frontend Page</h1>
    <button onclick="callBackend()">Call Backend</button>
    <p id="result"></p>

    <script>
        async function callBackend() {
            const res = await fetch("http://backend:5000/");
            const data = await res.json();
            document.getElementById("result").innerText = data.message;
        }
    </script>
</body>
</html>
```

---

# ⚡ Step 4: Frontend Dockerfile (Nginx + Multi-stage)

```dockerfile
# ---- Build stage (optional for real apps) ----
FROM nginx:alpine

# Remove default config
RUN rm /usr/share/nginx/html/*

# Copy static files
COPY index.html /usr/share/nginx/html/index.html

# Use non-root (nginx already uses non-root internally)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

# 🔗 Step 5: Docker Compose with Custom Network

## `docker-compose.yml`

```yaml
version: "3.9"

services:
  backend:
    build:
      context: ./backend
    container_name: backend
    networks:
      - app-network
    ports:
      - "5000:5000"

  frontend:
    build:
      context: ./frontend
    container_name: frontend
    networks:
      - app-network
    ports:
      - "8080:80"
    depends_on:
      - backend

networks:
  app-network:
    driver: bridge
```

---

# 🚀 Step 6: Enable BuildKit

BuildKit improves caching and performance.

## Linux / Mac

```bash
export DOCKER_BUILDKIT=1
```

## Or inline:

```bash
DOCKER_BUILDKIT=1 docker compose build
```

---

# ▶️ Step 7: Run the Application

```bash
docker compose up --build
```

---

# 🌍 Access

* Frontend → [http://localhost:8080](http://localhost:8080)
* Backend → [http://localhost:5000](http://localhost:5000)

---

# 🔐 Step 8: Key DevOps Concepts Used

## ✅ Multi-stage builds

* Reduce final image size
* Separate build & runtime

## ✅ Slim images

* `python:slim` instead of full image
* Smaller attack surface

## ✅ Non-root user

* Security best practice
* Prevent container privilege escalation

## ✅ Custom network

* Services communicate via DNS:

  ```
  http://backend:5000
  ```

## ✅ BuildKit

* Better caching
* Parallel builds
* Secrets support (advanced)

---

# 🧠 Optional Improvements (Advanced Practice)

## 1. Distroless Backend

Replace runtime stage with:

```dockerfile
FROM gcr.io/distroless/python3
```

⚠️ Requires:

* No shell
* Pre-installed dependencies only

---

## 2. Healthcheck

Healthcheck added in Dockerfile:

```
# Use python for healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python3 -c "import requests; requests.get('http://localhost:5000')" || exit 1
 ```

Purpose: Docker monitors your backend container and marks it healthy or unhealthy based on response.

Check the current health status:

docker inspect --format='{{json .State.Health}}' backend

Example output:
```
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2026-03-21T10:05:49.123456789+01:00",
      "End": "2026-03-21T10:05:49.150123456+01:00",
      "ExitCode": 0,
      "Output": ""
    }
  ]
}
```


Notes:

"Status": "starting" → initial state before first healthcheck runs

"Status": "unhealthy" → container failed healthcheck (check logs, maybe backend not running or curl missing)

"FailingStreak" → number of consecutive failed healthchecks

"Log" → history of healthcheck attempts

Tip: After adding healthcheck, make sure curl/needed python dependencies is installed in slim images.

---

## 3. .dockerignore

```
__pycache__/
*.pyc
node_modules/
.git
```

---

## 4. Environment Variables

```yaml
environment:
  - FLASK_ENV=production
```

---

# ✅ Summary

You now have:

* Minimal **Python backend**
* Lightweight **Nginx frontend**
* Secure containers (**non-root**)
* Optimized images (**multi-stage + slim**)
* Full orchestration (**Docker Compose + network**)