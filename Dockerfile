FROM python:3.8-slim-buster

WORKDIR /home/klee

# Install system utilities
RUN apt update
RUN yes | apt install gcc  python3-dev

# Create python environment
RUN python3 -m venv python

# Install python virtual environment dependancies
RUN python/bin/python3 -m pip install --upgrade pip
RUN python/bin/pip install wheel
RUN python/bin/pip install uwsgi
COPY requirements.txt repo/requirements.txt
RUN python/bin/pip install -r repo/requirements.txt

# Copy project source code inside of the container
COPY klee_engine /home/klee/repo/klee_engine

# Set up Flask environment variables: wsgi file path
# and environment mode
ENV FLASK_APP /home/klee/repo/klee_engine/application/wsgi.py
ENV FLASK_ENV development

# Copy deployment configuration files
COPY deploy/uwsgi.ini /home/epoklee/conf/uwsgi.ini
COPY deploy/entrypoint.sh entrypoint.sh
RUN chmod u+x ./entrypoint.sh

# Provide an entrypoint file path which will be run
# when `docker-compose up` is  executed
ENTRYPOINT ["./entrypoint.sh"]
