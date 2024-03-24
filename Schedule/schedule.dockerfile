# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY schedule_requirements.txt ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r schedule_requirements.txt

# Copy the application code to the working directory
COPY ./Schedule.py .

# Set the command to run the application
CMD ["python", "Schedule.py"]