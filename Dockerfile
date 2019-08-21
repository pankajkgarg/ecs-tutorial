# Dockerfile

# Using alpine for smallest size, use "python:3.7-slim" for ubuntu
FROM alpine AS base 

# Adding python3 for alpine
RUN apk --update add --no-cache python3

RUN pip3 install pipenv

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Adding Pipfiles 
COPY Pipfile*  /app/


RUN set -ex && pipenv install --deploy --system


COPY . /app



# ARG vs ENV https://vsupalov.com/docker-arg-vs-env/

ARG FLASK_ENV="production"

ENV FLASK_APP="app:app" \
	FLASK_PORT=80 \
	FLASK_ENV="${FLASK_ENV}"

EXPOSE $FLASK_PORT

# By default this command will run;  Can be overridden by docker run
CMD flask run --host=0.0.0.0 --port $FLASK_PORT
