# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY notification_requirements.txt ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r notification_requirements.txt

# Copy the application code to the working directory
COPY ./Notification.py .

# Set the command to run the application
CMD ["python", "Notification.py"]
