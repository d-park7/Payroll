# Pulls base python image from docker hub
FROM python:3.9.1-buster

# Create working directory
RUN mkdir -p /app

# Set working directory
WORKDIR /app

# Copy local directory to an app folder in container
# Destination directory will be the working directory
COPY . .

# Install required packages for the project
RUN pip install -r requirements.txt

# Initialize database and insert test data
RUN python initdb.py -n payroll.db -c
RUN python testinput.py -n payroll.db

# Start flask server
CMD [ "python", "app.py" ]