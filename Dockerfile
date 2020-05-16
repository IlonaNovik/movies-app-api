FROM python:3.8-alpine
MAINTAINER Ilona Novik

ENV PYTHONUNBUFFERED=0

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN pip install requests
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

RUN adduser -D user
USER user