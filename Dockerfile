FROM cimg/python:3.9.7-node

USER root
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath
RUN python3 -m pipx completions 

RUN npm install -g ganache-cli

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

RUN /bin/bash -c "source /root/.bashrc"

RUN pipx install eth-brownie

WORKDIR /code
