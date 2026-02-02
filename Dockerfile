# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your backend code into the container
COPY backend/ .

# Expose the port Hugging Face uses
EXPOSE 7860

# Command to run when the space starts:
# 1. Run Django database migrations.
# 2. Start the Gunicorn web server.
CMD sh -c "python manage.py migrate && gunicorn chem_vis_project.wsgi:application --bind 0.0.0.0:7860"
