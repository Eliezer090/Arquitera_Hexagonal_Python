FROM python:3.10-slim

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"


# Set working directory
WORKDIR /app

# Copy poetry files
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Copy the rest of the application code
COPY /src/. /app

# Set the Flask app environment variable
ENV FLASK_APP=main.py

# Start the Flask app
CMD if [ "$YOUR_ENV" = production ]; then \
        gunicorn main:app -b 0.0.0.0:8080; \
    else \
        flask run --host 0.0.0.0 --port 8080; \
    fi



