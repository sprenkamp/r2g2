# FastAPI Application with Docker-Compose

This demonstrates how to run the chatbot application via FastAPI using Docker Compose.


## Setup and Run

1. **Clone the repository**

    ```
    git clone https://github.com/sprenkamp/r2g2.git
    ```

2. **Navigate to the project directory**

    ```
    cd src/machine_learning/chat/docker
    ```

3. **Build and Run the Docker Containers**

    ```bash
    docker-compose up --build -d
    ```

After running this command, Docker Compose will set up two containers based on the `chat_fastapi.dockerfile` and `docker-compose.yml` 

## Access the API

You can test the application by sending a POST request e.g.:
    ```bash
    curl -X 'POST' 'http://{EXTERNAL IP ADRESSE}:8000/query' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "start_date": "2023-08-01",
    "end_date": "2023-08-30",
    "country": "Switzerland",
    "state": "Zurich",
    "query": "What are the main problems of Refugees in Zurich",
    "chat_history": []
    }'
    ```

## Stopping the Application

To stop the Docker Compose services:

    ```bash
    docker-compose down
    ```

