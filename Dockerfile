FROM node:14-alpine3.14

RUN apk add --no-cache git bash python3

WORKDIR /codeslide

# setup the server
COPY . .

RUN npm i
RUN echo -e "\nVITE_SERVER_URL=/." >> ./.env
RUN npm run build
RUN cp ./.env ./dist/

# setup the front-end
RUN cd ./dist/ && git clone https://github.com/code-slide/ui.git

# setup react app
RUN cd ./dist/ui && echo "VITE_SERVER_URL=/." > ./.env
RUN cd ./dist/ui && rm -rf ./package-lock.json
RUN cd ./dist/ui && npm install
RUN cd ./dist/ui && npm run build

RUN rm -rf ./tmp && mkdir ./tmp
RUN chmod -R a+rw ./tmp

USER node
EXPOSE 5001/tcp

CMD ["node", "./dist/index.js"]