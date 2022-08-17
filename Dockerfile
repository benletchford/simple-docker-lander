FROM python:3.10

WORKDIR /usr/src/app

COPY simple-docker-lander.py simple-docker-lander.py
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv
RUN pipenv install --system

ENTRYPOINT python simple-docker-lander.py
