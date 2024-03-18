# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY AMQP_requirements.txt ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r AMQP_requirements.txt

# Copy the application code to the working directory
COPY ./NotificationAMQP.py ./amqp_connection.py ./

# Set the command to run the application
CMD ["python", "NotificationAMQP.py"]
