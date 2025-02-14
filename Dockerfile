# Step 1: Use the official Python image from Docker Hub
FROM python:3.9-slim

# Step 2: Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Step 3: Install dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the application code into the container
COPY . /app

# Step 5: Expose the port for the Flask app
EXPOSE 8000

# Step 6: Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
