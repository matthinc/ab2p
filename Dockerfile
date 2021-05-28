FROM python:3.8.8-alpine3.13

RUN pip3 install natsort

RUN apk add caddy bash

WORKDIR /opt

COPY ./Caddyfile .
COPY ./import.py .

CMD ["/bin/bash", "-c", "python3 -u import.py && caddy run"]