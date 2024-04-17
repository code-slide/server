FROM node:14-alpine3.14
ARG ENV

RUN apk add --no-cache git bash python3
WORKDIR /codeslide
COPY . .

# Setup the back-end
RUN npm i
RUN echo -e "\nVITE_SERVER_URL=/." >> ./.env
RUN npm run build
RUN cp ./.env ./dist/

# Setup the front-end
COPY ui.sh ui.sh
RUN chmod +x ui.sh && ./ui.sh

RUN rm -rf ./tmp && mkdir ./tmp
RUN chmod -R a+rw ./tmp

USER node
EXPOSE 5001/tcp

CMD ["node", "./dist/index.js"]