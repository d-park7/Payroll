# Pulls base python image from docker hub
FROM python:3.8.5-slim-buster

# Create working directory
RUN mkdir -p /app

# Set working directory
WORKDIR /app

# Copy local directory to an app folder in container
# Destination directory will be the working directory
COPY . .

# Install required packages for the project
RUN pip3 install -r requirements.txt

# Start flask server
CMD [ "python3", "app.py" ]