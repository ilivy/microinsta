FROM node:14-alpine
# USER node
WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD [ "npm", "start" ]