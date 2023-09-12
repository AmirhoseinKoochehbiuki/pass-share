# pull official base image
# FROM python:3.11.4-slim-buster
# FROM python:3.12.0rc2-alpine3.18
FROM python:3.11.0-alpine as builder


# add user
RUN addgroup app && adduser -S -G app app
USER app

# set work directory
WORKDIR /app

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install postgres client
# RUN apk add --update --no-cache postgresql-client

# port in container
EXPOSE 8000

# copy project
COPY . .

# Run command
# CMD [ "python3" , "manage.py" , "runserver" ]

