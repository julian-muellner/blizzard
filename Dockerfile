FROM movesrwth/storm:1.7.0

LABEL maintainer="Julian Muellner (TU Wien)"

WORKDIR /var
COPY . /var/blizzard
WORKDIR /var/blizzard

RUN apt-get install python3-pip -y
RUN chmod +x /var/blizzard/blizzard.py
RUN pip install -r /var/blizzard/requirements.txt

ENTRYPOINT bash

