FROM python:3.11.4-alpine

WORKDIR /usr/src/app/ds-project/ds-core

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Install system dependencies
RUN apk update && \
    apk add --no-cache build-base linux-headers musl-dev && \
    apk add --no-cache gdal-dev geos-dev postgresql-dev && \ 
    rm -rf /var/cache/apk/*


COPY ./requirements.txt /usr/src/app/ds-project/ds-core/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/ds-project/ds-core/entrypoint.sh

COPY . /usr/src/app/ds-project/ds-core/
ENTRYPOINT [ "/usr/src/app/ds-project/ds-core/entrypoint.sh" ]
