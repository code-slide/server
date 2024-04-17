#!/bin/sh

if [ "${ENV}" = 'DEV' ]; then 
    cd ./dist && git clone https://github.com/code-slide/ui.git -b toolbar
    cd ui && echo "VITE_SERVER_URL=/." > .env
    rm -rf package-lock.json
    npm install && npm run build
    cd ../..
fi