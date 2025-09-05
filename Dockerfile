FROM python:3.12-slim

# Create working directory
WORKDIR /job_search

# Install dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set environment variables
ENV FLASK_APP=job_search:create_app
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Entrypoint: wait for DB, run migrations, then start Flask
CMD flask db upgrade && flask run --host=0.0.0.0 --port=5000