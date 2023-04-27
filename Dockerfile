# Base image
FROM python:alpine3.17

# Set working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY bot.py .

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "bot.py"]
