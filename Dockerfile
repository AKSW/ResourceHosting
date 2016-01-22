FROM ubuntu:latest

MAINTAINER Norman Radtke <radtke@informatik.uni-leipzig.de>

ENV DEBIAN_FRONTEND noninteractive

# http://jaredmarkell.com/docker-and-locales/
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# update ubuntu as well as install python3
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -qy python3 python3-pip && \
    apt-get clean
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip


ENV LDOW_HOME /opt/ldow
RUN mkdir $LDOW_HOME
WORKDIR $LDOW_HOME
COPY ldowapi.py $LDOW_HOME/ldowapi.py
RUN chmod +x $LDOW_HOME/ldowapi.py
COPY requirements.txt $LDOW_HOME/requirements.txt
COPY lib $LDOW_HOME/lib
RUN pip install -r requirements.txt
RUN ln -s $LDOW_HOME/ldowapi.py /usr/local/bin/ldowapi

RUN mkdir /data
COPY start.nq /data/graph.nq

VOLUME /data
EXPOSE 80

ENV RDF_SER nquads
ENV GRAPH_FILE /data/graph.nq
CMD /opt/ldow/ldowapi.py $GRAPH_FILE --input $RDF_SER
