# Stage 1: build the React bundle with Node. Nothing from this stage except dist/ reaches the runtime image.
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: serve the static bundle with nginx as a non-root user (uid 101) on port 8080.
FROM nginxinc/nginx-unprivileged:1.31-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
# The entrypoint renders the template with envsubst, so the backend address is configuration, not code.
ENV BACKEND_HOST=backend BACKEND_PORT=8000 NGINX_ENTRYPOINT_LOCAL_RESOLVERS=1 NGINX_ENVSUBST_FILTER="^(BACKEND_|NGINX_LOCAL_RESOLVERS)"
EXPOSE 8080
