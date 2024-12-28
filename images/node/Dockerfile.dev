# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY ./client/package.json ./
COPY ./client/package-lock.json ./

RUN npm install

COPY ./client .

RUN npm run build

EXPOSE 8080

CMD ["npm", "run", "serve"]
