FROM python:3.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

WORKDIR /pybuilder-radon

COPY . /pybuilder-radon/

RUN apk --update --no-cache add gcc libc-dev libffi-dev openssl-dev
RUN pip install pybuilder
RUN pyb install_dependencies
RUN pyb install
