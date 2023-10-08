# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables needed for Poetry
ENV POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Install gunicorn
RUN pip install gunicorn

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock /app/

# Install app dependencies
RUN poetry install --no-dev

# Copy the current directory contents into the container
COPY . /app

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run gunicorn when the container launches
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "-w", "4"]
