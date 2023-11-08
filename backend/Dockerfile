FROM node:lts-alpine3.18

RUN mkdir /app
WORKDIR /app

RUN npm install -g nodemon

COPY ./package*.json ./
RUN npm install

COPY . .

CMD node app.js
