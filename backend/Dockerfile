FROM python:3.7.10-slim-buster

ADD . /usr/tc/backend
WORKDIR /usr/tc/

RUN pip install --upgrade pip && pip install --no-cache-dir -r ./backend/requirements.txt


ENV PYTHONPATH=$PYTHONPATH::/usr/tc/backend/travell_companion:/usr:/usr/tc
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000
