# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# RUN apt-get install ffmpeg libsm6 libxext6  -y

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Streamlit-specific commands for running the app
CMD streamlit run app.py --server.enableXsrfProtection false --server.port $PORT auth_token.py