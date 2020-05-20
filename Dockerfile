FROM python:3.8-alpine
MAINTAINER Ilona Novik

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN pip install requests
RUN pip install django-rest-swagger
RUN pip install coreapi pyyaml
RUN pip install django-filter
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN adduser -D user
USER user

CMD ["gunicorn", "app.wsgi"]