# pull official base image
FROM python:3.9.1-slim-buster

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# set work directory
RUN mkdir /central
WORKDIR /.

# copy project
COPY ./central /central

CMD python3 central/events.py
