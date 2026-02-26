# Use the official image as a parent image (use a fixed, up-to-date Debian slim tag)
FROM python:3-slim

# Update OS packages to ensure security patches are applied
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=wsgi.py

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
