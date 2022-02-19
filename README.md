# bremen-classifieds-api

Thin API layer on top of https://schwarzesbrett.bremen.de/, still work in progress.

## How to

Run with docker-compose:

```shell
$ cp .env.example .env
$ docker-compose up --build
```

## API

Get all available categories:

```shell
$ curl localhost:5000/api/categories/
```

Get classifieds from a category:

```shell
$ curl localhost:5000/api/categories/4
```

Filter classifieds by either `search`, `has_picture`, `is_commercial` or `updated_since:

```shell
$ curl localhost:5000/api/categories/1?has_picture=1&search=P%C3%A4dagoge&is_commercial=0&updated_since=2022-02-19 08:00:00
```