FROM python:3.9

# Create and set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port the FastAPI application will run on
EXPOSE 80

WORKDIR /app/dnarchive_server

# Start the FastAPI application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
