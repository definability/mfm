FROM python:3

COPY install-dependencies.sh /install-dependencies.sh
RUN /install-dependencies.sh

