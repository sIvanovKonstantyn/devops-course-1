# 🐳 Dockerfile Debug Checklist

## 🚫 1. Container Doesn’t Start

### ✅ Check logs first

```bash
docker logs <container_id>
```

* Look for:

  * Missing dependencies
  * Syntax errors
  * Wrong command/entrypoint

---

### ✅ Verify ENTRYPOINT / CMD

Common mistakes:

* Wrong executable path
* Script not executable

```dockerfile
CMD ["node", "app.js"]   # ✅ preferred (exec form)
# vs
CMD node app.js          # ❌ shell form (can cause issues)
```

Check:

```bash
docker inspect <container_id>
```

---

### ✅ Check file permissions

If using scripts:

```dockerfile
RUN chmod +x start.sh
```

---

### ✅ Test container interactively

```bash
docker run -it --entrypoint sh <image>
```

Then manually run your command inside.

---

## 🌐 2. Port Not Accessible

### ✅ Check port mapping

```bash
docker ps
```

You should see:

```
0.0.0.0:3000->3000/tcp
```

If not:

```bash
docker run -p 3000:3000 <image>
```

---

### ✅ Ensure app binds to 0.0.0.0 (NOT localhost)

❌ Wrong:

```js
app.listen(3000, 'localhost')
```

✅ Correct:

```js
app.listen(3000, '0.0.0.0')
```

---

### ✅ EXPOSE is not enough

```dockerfile
EXPOSE 3000
```

👉 This is documentation only — you still need `-p`.

---

## 🔁 3. Container Exits Immediately

### ✅ Foreground process required

Container stops if main process exits.

❌ Bad:

```dockerfile
CMD ["service", "nginx", "start"]
```

✅ Good:

```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

---

### ✅ Check exit code

```bash
docker ps -a
```

Then:

```bash
docker inspect <container_id> | grep ExitCode
```

---

## 📦 4. Build Issues / Missing Files

### ✅ Check `.dockerignore`

You might be excluding needed files:

```
node_modules
.env
dist
```

---

### ✅ Verify COPY paths

```dockerfile
COPY . .
```

Debug:

```bash
docker build --no-cache .
```

---

### ✅ Inspect image contents

```bash
docker run -it <image> sh
ls -la
```

---

## 🔐 5. Environment Variables Not Working

### ✅ Check ENV vs runtime variables

```dockerfile
ENV NODE_ENV=production
```

Override:

```bash
docker run -e NODE_ENV=dev <image>
```

---

### ✅ Debug inside container

```bash
env
```

---

## 🧠 6. Dependency / Runtime Errors

### ✅ Rebuild without cache

```bash
docker build --no-cache -t myapp .
```

---

### ✅ Ensure correct base image

Example:

```dockerfile
FROM node:18-alpine
```

Alpine issues:

* Missing `glibc`
* Different package manager (`apk`)

---

### ✅ Install system dependencies

```dockerfile
RUN apk add --no-cache python3 make g++
```

---

## 🧪 7. Health Checks & Debugging Tools

### ✅ Add temporary debug tools

```dockerfile
RUN apk add curl
```

Test inside container:

```bash
curl localhost:3000
```

---

### ✅ Add HEALTHCHECK

```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:3000 || exit 1
```

---

## 🔍 8. Networking Issues

### ✅ Check container network

```bash
docker network ls
docker inspect <container_id>
```

---

### ✅ Test connectivity

From inside container:

```bash
ping other-service
```

---

## ⚙️ 9. Multi-stage Build Problems

### ✅ Ensure artifacts copied correctly

```dockerfile
COPY --from=builder /app/dist ./dist
```

Debug:

```bash
docker run -it <image> sh
```

---

## 🧼 10. General Best Practices

### ✅ Use small, clear layers

```dockerfile
RUN npm install
```

instead of chaining too much logic

---

### ✅ Pin versions

```dockerfile
FROM node:18.17.0
```

---

### ✅ Use non-root user

```dockerfile
USER node
```

---

### ✅ Add debug-friendly CMD during development

```dockerfile
CMD ["sh"]
```

---

# 🚀 Quick Debug Flow

1. `docker ps -a` → container status
2. `docker logs` → error output
3. `docker run -it --entrypoint sh` → manual debug
4. Check ports (`-p`, 0.0.0.0)
5. Rebuild with `--no-cache`