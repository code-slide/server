# CodeSlide's Server

These are the programs located on the backend of [codeslide.net](https://www.codeslide.net).

- /parser: A Python-powered Express program that returns a list of frames from user's script.
- /compiler: A Python-powered Express program that returns an HTML from a json of SVGs.

## Self-host instruction
```
docker build -t codeslide/dev --build-arg "ENV=DEV" .
docker run --name codeslide -d -p 8001:5001 -v ${PWD}/tmp:/codeslide/tmp codeslide/dev
```

## Testing instruction
```
pytest --cov=utils --cov-report term-missing utils/
```