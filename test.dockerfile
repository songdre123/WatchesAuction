# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY ./test_requirements.txt ./AMQP_requirements.txt ./amqp_connection.py ./test.py ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r test_requirements.txt -r AMQP_requirements.txt

# Set the command to run the application
CMD ["python", "test.py"]
