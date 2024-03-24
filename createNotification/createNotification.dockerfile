# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./createNotification.py  ./createNotification_requirements.txt ./invokes.py ./amqp_connection.py ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r createNotification_requirements.txt

# Set the command to run the application
CMD ["python", "createNotification.py"]
