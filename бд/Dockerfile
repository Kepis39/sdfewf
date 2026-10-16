FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir psycopg2-binary Faker

COPY generate_data.py .

# Wait for postgres to be ready or rely on docker-compose healthcheck
CMD ["python", "generate_data.py"]
