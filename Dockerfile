# Base image
FROM python:alpine3.17

# Set working directory
WORKDIR /app

# Copy the Python script into the container
COPY bot.py .

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "bot.py"]
