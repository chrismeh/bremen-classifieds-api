FROM python:alpine

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY bremen_classifieds_api ./bremen_classifieds_api

CMD ["flask", "run", "-h", "0.0.0.0"]