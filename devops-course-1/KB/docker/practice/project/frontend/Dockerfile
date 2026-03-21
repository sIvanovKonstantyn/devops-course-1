# ---- Build stage (optional for real apps) ----
FROM nginx:1.29.5-alpine3.23

# Remove default config
RUN rm /usr/share/nginx/html/*

# Copy static files
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Run nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]