FROM python:3.8.8-alpine3.13

RUN apk add bash

RUN pip3 install requests xmltodict

WORKDIR /opt

COPY ./test.py .

CMD ["/bin/bash", "-c", "python3 -u test.py"]