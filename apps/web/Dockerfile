# syntax=docker/dockerfile:1.7
# Build context: repository root.
FROM node:24-bookworm-slim AS deps
WORKDIR /repo
RUN corepack enable
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY apps/web/package.json apps/web/
RUN pnpm install --frozen-lockfile --filter @typeicon/web...

FROM deps AS build
COPY apps/web apps/web
COPY assets assets
RUN pnpm --filter @typeicon/web build

# One-shot migration runner (drizzle migrations in db/migrations).
FROM deps AS migrate
COPY apps/web apps/web
COPY db db
WORKDIR /repo/apps/web
CMD ["pnpm", "db:migrate"]

FROM node:24-bookworm-slim AS runner
ENV NODE_ENV=production
WORKDIR /app
RUN useradd --system --uid 1001 nextjs
COPY --from=build /repo/apps/web/.next/standalone ./
COPY --from=build /repo/apps/web/.next/static ./apps/web/.next/static
USER nextjs
EXPOSE 3107
CMD ["node", "apps/web/server.js"]
