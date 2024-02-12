# Use an official PostgreSQL image
FROM postgres:14

# Copy SQL scripts to initialize the database
COPY init.sql /docker-entrypoint-initdb.d/
