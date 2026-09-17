# ---- Dependencies: install node_modules once (cached) ----
FROM node:24-alpine AS deps
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

# ---- Dev runtime: hot-reload server ----
FROM node:24-alpine AS dev
WORKDIR /app
RUN corepack enable
ENV NODE_ENV=development
COPY --from=deps /app/node_modules /app/node_modules
COPY . .
EXPOSE 5173
CMD ["pnpm", "run", "dev", "--", "--host"]
