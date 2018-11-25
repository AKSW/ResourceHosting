FROM python:3

LABEL maintainer="Norman Radtke <radtke@informatik.uni-leipzig.de>, Natanael Arndt <arndtn@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive

RUN useradd -md /usr/src/app flask
USER flask
WORKDIR /usr/src/app

COPY lib/ /usr/src/app/lib
COPY ldowapi.py /usr/src/app/
COPY requirements.txt /usr/src/app/

USER root
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir uwsgi

ENV GRAPH_FILE /data/graph.nq
ENV GRAPH_SERIALIZATION nquads

RUN mkdir /data
COPY start.nq $GRAPH_FILE
RUN chown flask $GRAPH_FILE

VOLUME /data
EXPOSE 8080
CMD uwsgi --http 0.0.0.0:8080 --module ldowapi --callable app --pyargv "$GRAPH_FILE --input $GRAPH_SERIALIZATION"
