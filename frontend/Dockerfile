FROM node:22.11-alpine3.20

# current working directory
WORKDIR /app

COPY package.json .

RUN npm install

# copy files from users folder to /app folder
COPY . /app/

EXPOSE 3000

CMD ["npm", "run", "dev"]