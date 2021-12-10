# Pulls base python image from docker hub
FROM python:3.7

# Set working directory for docker container
WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run flask in debug mode
ENV FLASK_ENV=development

COPY requirements.txt requirements.txt

# Install required packages for the project
RUN pip install -r requirements.txt

EXPOSE 5000

# Copy local directory to an app folder in container
# Destination directory will be the working directory
COPY . .

# Start flask server
CMD ["flask", "run"]