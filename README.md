# bremen-classifieds-api

Thin API layer on top of https://schwarzesbrett.bremen.de/, still work in progress.

## How to

Run with Docker:
```shell
$ docker build -t classifieds:latest .
$ docker run -it --rm -p 5000:5000 classifieds:latest
```

Get all available categories:
```shell
$ curl localhost:5000/api/categories/
```

Get classifieds from a category:
```shell
$ curl localhost:5000/api/categories/verkauf-angebote/bildung-nachhilfe-verkauf
```

Filter classifieds by either `search`, `has_picture` or `is_commercial`:
```shell
$ curl localhost:5000/api/categories/verkauf-angebote/bildung-nachhilfe-verkauf?search=englisch&is_commercial=0&has_picture=1
```