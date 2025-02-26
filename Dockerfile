# Use an official Python image as the base
FROM python:3.13-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set the command to run the application
CMD ["python", "book_classes.py"]