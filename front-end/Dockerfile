FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:lts-alpine as production-stage
WORKDIR /app
COPY --from=build-stage /app/server .
RUN npm install
EXPOSE 4000
CMD ["node", "index.js"]