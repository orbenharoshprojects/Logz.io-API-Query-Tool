# Use the official Python image from the DockerHub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN mkdir /app/Downloads
#RUN mkdir /supportCLIMenu/supportCLIFiles

# Copy the application files to the container
COPY flask_app.py data_processor.py /app/

# Copy the HTML templates to the container
COPY templates/ /app/templates/

# Copy the static files to the container
COPY static/ /app/static/

# Install the required dependencies
RUN pip install flask requests

# Specify the port number the container should expose
EXPOSE 8000

# Run flask_app.py when the container launches
CMD ["python", "flask_app.py"]
