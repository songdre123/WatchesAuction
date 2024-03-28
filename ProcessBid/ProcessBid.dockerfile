# Use a base image with Python installed
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY ./ProcessBid_requirements.txt ./ProcessBid.py  ./amqp_connection.py ./
# Install any dependencies required by your application
RUN python -m pip install --no-cache-dir -r ProcessBid_requirements.txt

# Set the command to run your application
CMD ["python", "ProcessBid.py"]