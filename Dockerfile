# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /backend

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt


# Copy project files to the working directory
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]