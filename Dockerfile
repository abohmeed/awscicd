FROM 194371479148.dkr.ecr.eu-central-1.amazonaws.com/aws-node:latest
WORKDIR app
ADD index.js package.json ./
RUN npm install
EXPOSE 3000
ENTRYPOINT ["node","index.js"]
