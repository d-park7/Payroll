# Pulls base python image from docker hub
FROM python:3.9.1-buster

# Set working directory
WORKDIR /app

# Copy local directory to an app folder in container
COPY . /app

RUN pip install -r requirements.txt

