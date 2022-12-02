FROM blizzard-base:latest

LABEL maintainer="Julian Muellner"

WORKDIR /opt/blizzard
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x blizzard.py

ENTRYPOINT bash

