FROM python:3

COPY ./scripts/install-dependencies.sh /install-dependencies.sh
RUN /install-dependencies.sh

WORKDIR /src
