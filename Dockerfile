# Use Python 3.10.11 slim as the base image
FROM python:3.10.11-slim
 
# Install system dependencies and curl for installing Poetry
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Install
 
# Prevents Python from writing pyc files to disk & buffering stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
 
# Install Poetry using the official installer
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.0
 
# Set Poetry environment variables to disable virtual environments
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    PATH="/root/.local/bin:$PATH"
 
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    sqlite3 \
    libsqlite3-mod-spatialite \
    gdal-bin \
    libgdal-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
 
ENV PYTHONPATH=/app
   
# Change directory to the Django project folder
WORKDIR /app/
 
# Copy the entire project into the container (filter .dockerignore folders and files)
COPY . /app
 
# # Deshabilitamos keyring para que no cuelgue
# ENV PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
 
# # Opcional: configuración permanente de Poetry
# RUN poetry config keyring.enabled false
 
# # Para evitar el que se quede colgado resolviendo HTTPS pypi
# RUN poetry cache clear PyPI --all
# RUN poetry cache clear _default_cache --all
 
# Lock con máxima verbosidad y sin interacción
RUN poetry lock -vvv --no-interaction
 
# Install poetry dependencies without a virtual environment
RUN poetry install --no-interaction --no-ansi

# Make migrations
RUN poetry run poe makemigrations
 
# Development
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]