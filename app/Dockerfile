# Stage 1: Build frontend
FROM node:latest as build-stage
WORKDIR ./app
COPY ./package.json /app/
RUN npm install
COPY ./ /app/

EXPOSE 3000

RUN npm run build --output-path=./dist/out
RUN npm run dev

# Stage 2: Serve it using Ngnix
#FROM nginx:stable-alpine
#COPY --from=build-stage /app/.svelte-kit/output/server /usr/share/nginx/html
