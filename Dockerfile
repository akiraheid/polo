FROM docker.io/node:17-alpine
EXPOSE 8080
ENTRYPOINT ["node", "polo.js"]
COPY polo.js polo.js
