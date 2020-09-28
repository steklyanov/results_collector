FROM python:3.7.3-slim-stretch
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install gcc libpq-dev python-flower \
                       build-essential g++ cmake make git \
                       libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    pip install --upgrade pip

ADD requirements.txt /config/
RUN pip install -r /config/requirements.txt
RUN mkdir /backend
RUN mkdir /backend/documents
WORKDIR /backend
