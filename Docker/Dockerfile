FROM python:3.9
MAINTAINER Andrey Tikhonov "andrey.tikhonov@ukr.net"

RUN apt-get update
RUN apt-get install git curl pipenv -y
RUN bash -c 'git clone https://github.com/pydeveloper-t/yahoo_scraper.git /yahoo; cd /yahoo;pipenv install'
WORKDIR /yahoo
ENTRYPOINT ["/yahoo/start.sh"]

