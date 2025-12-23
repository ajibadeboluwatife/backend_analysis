# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
COPY tsconfig.json tsconfig.node.json vite.config.ts ./

RUN npm install

COPY src ./src
COPY index.html ./

RUN npm run build

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /app/dist

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/index.html || exit 1

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]