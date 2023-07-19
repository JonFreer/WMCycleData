# stage: dependencies
FROM node:20 AS dependencies

WORKDIR /app/
# removed yarn.lock
COPY package.json /app/ 
RUN npm install

# stage: builder
FROM dependencies AS builder
COPY ./ /app/
ARG REACT_APP_HOST
RUN npm run build

# stage: prod
FROM nginx:latest AS prod
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build/ /usr/share/nginx/html/

# stage: dev
FROM dependencies AS dev
ARG REACT_APP_HOST
ENV REACT_APP_HOST=${REACT_APP_HOST}
COPY ./ /app/
CMD PORT=80 yarn start