FROM python:3.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /pybuilder-radon

COPY . /pybuilder-radon/

RUN pip install pybuilder
# RUN pyb install_dependencies
# RUN pyb install
