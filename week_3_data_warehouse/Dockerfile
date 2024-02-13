FROM python:3.9

RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir pandas psycopg2 sqlalchemy requests pyarrow

# Copy the Python script into the image
WORKDIR /app
COPY import.py import.py

# Set environment variables
ENV P_HOST=host.docker.internal
ENV P_PORT=3212
ENV P_NAME=green_taxi
ENV P_USER=bodhi
ENV P_PASSWORD=bodhi

# Run the Python script when the container starts
CMD ["python", "import.py"]