FROM node:22.11-alpine3.20

WORKDIR /app

COPY package.json .

RUN npm install

COPY . /app/

EXPOSE 3000

CMD ["npm", "run", "dev"]