FROM python:3.8.8-alpine3.13

RUN pip3 install natsort Jinja2

RUN apk add caddy bash

WORKDIR /opt

COPY ./Caddyfile.j2 .
COPY ./import.py .

CMD ["/bin/bash", "-c", "python3 -u import.py && caddy run"]