FROM node:21-alpine

# Install xdg-utils
RUN apk add --no-cache xdg-utils

WORKDIR /app

COPY package.json .

RUN npm install --force

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]