FROM ubuntu:18.04

ENV PYTHONIOENCODING UTF-8
ENV LANG C.UTF-8

RUN apt-get update -y \
 && apt-get install -y \
    python3 \
    python3-pip \
    git

RUN cd /home/ && git clone https://github.com/seven48/vk_audios_bot

COPY ./docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

WORKDIR /home/vk_audios_bot

ENTRYPOINT docker-entrypoint.sh
