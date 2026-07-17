FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
COPY apps/web/package.json ./apps/web/package.json
COPY apps/web/vite.config.ts ./apps/web/vite.config.ts
COPY apps/web/index.html ./apps/web/index.html
COPY apps/web/src ./apps/web/src

RUN npm install
RUN npm run build --workspace apps/web

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/apps/web/dist ./dist
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
