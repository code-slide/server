#!/bin/sh

if [ "${ENV}" = 'DEV' ]; then 
    cd ./dist && git clone -b seo https://github.com/code-slide/ui.git
    cd ui && echo "VITE_SERVER_URL=/." > .env
    rm -rf package-lock.json
    npm install && npm run build
    cd ../..
fi