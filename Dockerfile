FROM python:3.10.3-alpine

RUN apk update
RUN apk add gcc libressl-dev libffi-dev musl-dev curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"
RUN poetry config virtualenvs.create false


WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN apk --no-cache add --virtual build-deps build-base libffi-dev
RUN poetry install --no-dev
RUN apk del build-deps

COPY . /app

EXPOSE 9999
CMD gunicorn "run:_create_wsgi_app('prod')" -b 0.0.0.0:9999 -k gevent --timeout 180
