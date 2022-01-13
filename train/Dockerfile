# pull official base image
FROM python:3.9.1-slim-buster

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# set work directory
RUN mkdir /train
WORKDIR /.

# copy project
COPY ./train /train
COPY . .

CMD celery --app=train.tasks.celery worker -Q station,speed --loglevel=info -E && celery beat --app=train.tasks.celery --loglevel=info
