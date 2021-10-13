FROM ubuntu:20.04

#install
RUN \ 
  sed --in-place 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential
#RUN \
#  apt-get install -y software-properties-common
RUN \ 
  apt-get install -y vim

ENV DEBIAN_FRONTEND=noninteactive

RUN \
  apt-get install -y texlive-publishers

#RUN \
#  apt-get install -y gnuplot

RUN \
 rm -rf /var/lib/apt/lists/*

RUN \
  mkdir /home/paper

WORKDIR /home/paper

COPY paper1.tex .
COPY Makefile .
#CMD  ["make"]
#CMD  ["make","clean"]
