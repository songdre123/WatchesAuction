# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY user_requirements.txt ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r user_requirements.txt

# Copy the application code to the working directory
COPY ./Users.py .

# Set the command to run the application
CMD ["python", "Users.py"]
