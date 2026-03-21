# syntax=docker/dockerfile:1.6

# ---- Builder stage ----
FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Runtime stage ----
FROM python:3.14-slim

# Use python for healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python3 -c "import requests; requests.get('http://localhost:5000')" || exit 1

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

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]