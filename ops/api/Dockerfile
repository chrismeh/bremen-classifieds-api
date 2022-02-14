FROM python:alpine

ENV FLASK_APP=bremen_classifieds_api.app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY bremen_classifieds_api ./bremen_classifieds_api

CMD ["flask", "run", "-h", "0.0.0.0"]