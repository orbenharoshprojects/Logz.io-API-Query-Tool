# Use a more specific base image to reduce image size
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Create necessary directories
RUN mkdir /app/Downloads

# Copy the application files to the container
COPY flask_app.py data_processor.py /app/

# Copy the HTML templates to the container
COPY templates/ /app/templates/

# Copy the static files to the container
COPY static/ /app/static/

# Copy the updated requirements.txt
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the port number the container should expose
EXPOSE 8000

# Use gunicorn as the entrypoint to serve your application
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "flask_app:app", "--threads", "4"]
