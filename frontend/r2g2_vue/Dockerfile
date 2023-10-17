FROM node:14.20.1 AS build
WORKDIR /build
COPY . .
RUN npm i --registry=https://registry.npmmirror.com
RUN npm run build

FROM nginx:1.21.6
COPY --from=build /build/dist /usr/share/nginx/html
COPY --from=build ./build/conf.d /etc/nginx/conf.d