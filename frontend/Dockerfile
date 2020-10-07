FROM node:alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN apk update && apk add python3 make g++
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:1.18.0-alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
ADD nginx/default.conf etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]
