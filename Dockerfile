# Use the official Miniconda3 base image
FROM continuumio/miniconda3

# Set working directory for the whole project
WORKDIR /app

# Copy environment.yml and create conda environment
COPY environment.yml /app/
RUN conda env create -f environment.yml

# Install Gunicorn in the created environment
RUN conda run -n mlops-california-housing pip install gunicorn

# Expose Flask port
EXPOSE 5001

# Copy all project files (including models, config, api, etc.)
COPY . /app/

# Set working directory to api for Flask app
WORKDIR /app/api

# Environment variables for model path and Flask
ENV MODEL_PATH=/app/models
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run Flask app with Gunicorn using the conda environment
CMD ["conda", "run", "-n", "mlops-california-housing", "gunicorn", "--bind", "0.0.0.0:5001", "app:app"]


