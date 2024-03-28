# CodeSlide's Server

These are the programs located on the backend of [codeslide.net](https://www.codeslide.net).

- /parser: A Python-powered Express program that returns a list of frames from user's script.
- /compiler: A Python-powered Express program that returns an HTML from a json of SVGs.

## Self-host
```
docker build -t codeslide/app .
docker run --name codeslide -d -p 8001:5001 -v ${PWD}/tmp:/codeslide/tmp codeslide/app
```