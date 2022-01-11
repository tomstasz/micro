# pull official base image
FROM python:3.9.1-slim-buster

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# set work directory
RUN mkdir /lineman
WORKDIR /.

# copy project
COPY ./lineman /lineman

EXPOSE 5000

CMD python3 lineman/views.py
