# Use a base image with Python installed
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the required files into the container
COPY ./processWinner_requirements.txt ./processWinner.py ./invokes.py ./

# Install any dependencies required by your application
RUN python -m pip install --no-cache-dir -r processWinner_requirements.txt

# Set the command to run your application
CMD ["python", "processWinner.py"]