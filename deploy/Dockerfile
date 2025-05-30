# Use a slim Python 3.12 base image
FROM python:3.12-slim

# Install deps
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install the `uv` tool for dependency management and fast installs
RUN pip install uv==0.6.0

# Set working directory inside the container
WORKDIR /app

# Copy the service_A code into the container
COPY ./ /app/

# Install dependencies using uv and the service's pyproject.toml
# This assumes dependencies are resolvable from the context and any lock file is already handled
RUN uv pip install --no-cache --system -r requirements.lock

ENV PYTHONPATH=/src
# Run the application
# Note: adjust the path if main.py is nested under src/service_a
CMD python src/app/main.py