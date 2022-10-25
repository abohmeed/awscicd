FROM node:13-alpine
WORKDIR app
ADD index.js package.json ./
RUN npm install
EXPOSE 3000
ENTRYPOINT ["node","index.js"]
