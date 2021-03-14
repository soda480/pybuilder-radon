FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /pybuilder-radon

COPY . /pybuilder-radon/

RUN pip install pybuilder
RUN pyb
