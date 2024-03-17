# Use a base image with Python installed
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY processWinner.py .
COPY invokes.py .
COPY processWinner_requirements.txt ./

# Install any dependencies required by your application
RUN pip install --no-cache-dir -r processWinner_requirements.txt

# Set the command to run your application
CMD ["python", "processWinner.py"]