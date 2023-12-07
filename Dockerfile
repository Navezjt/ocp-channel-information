# Use the official Python image with pipenv installed
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --ignore-pipfile

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 for the Flask app (only used when running the API)
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=app.py
ENV API_MODE=false

# Run app.py when the container launches
CMD ["sh", "-c", "if [ \"$API_MODE\" == \"true\" ]; then pipenv run flask run --host=0.0.0.0 --port=5000; else pipenv run python app.py; fi"]
