# Step 1: Use an official Python base image from Docker Hub
FROM python:3.10-slim

# Step 2: Set a working directory for the application inside the container
WORKDIR /

# Step 3: Copy dependency files (like poetry.lock and pyproject.toml)
COPY pyproject.toml poetry.lock /

# Step 4: Install Poetry package manager
RUN pip install --no-cache-dir poetry

# Step 5: Install application dependencies using Poetry
RUN poetry install --no-root

# Step 6: Copy the rest of the application code
COPY . /

# Step 7: Expose the port on which FastAPI will run
EXPOSE 8000

# Step 8: Define the command to run your FastAPI app
CMD ["poetry","run","uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
