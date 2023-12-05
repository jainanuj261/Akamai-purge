# Use the official Python image as a base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install "python-dotenv[cli]"

# Copy your Python application files to the container
COPY . .

# Command to run your application
CMD ["python", "purge.py"]

