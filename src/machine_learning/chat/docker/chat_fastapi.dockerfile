# Use the official image as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run your code when the container launches
CMD ["uvicorn", "chat_fastapi_new:app", "--host", "0.0.0.0", "--port", "8000"]
