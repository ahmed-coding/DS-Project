FROM python:3.11.4-alpine

WORKDIR /usr/src/app/ds-project/ds-celeryworker

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/ds-project/ds-celeryworker/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app/ds-project/ds-celeryworker/