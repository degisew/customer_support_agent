# AI Customer Support Agent

An AI-powered Customer Support Agent built with FastAPI and Google Gemini API, designed to automate first-line customer interactions.

## Prerequisites

Ensure the following tools are installed on your machine before proceeding:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone git@github.com:degisew/customer_support_agent.git
cd customer_support_agent
```

### 2. Create a `.env` File

Create a `.env` file in the root of your project directory. This file will contain environment variables for the FastAPI API. Here's an example `.env` file:

```bash
# FastAPI
API_KEY=<your-api_key-here>
```

Make sure to replace `<your-api_key-here>` with valid data.

### 3. Build and Run the Containers

Use Docker Compose to build and spin up the containers:

```bash
docker-compose up --build
```

this command will build and run a container For:

- **FastAPI application** (An API server)

### 4. Access the Services

- **FastAPI API**: Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to access the FastAPI API docs.

## Project Structure

```bash
├── docker
│     └── dev/          
│          └── Dockerfile # FastAPI API Dockerfile for development environment
├── requirements/         # contains a requirement files for separate environments
├── src/                  # Custom Apps collection
├── docs/                 # Documentation files
├── scripts/              # Custom scripts for automating tasks
├── .env                  # Environment variables (you will create this)
├── compose.yaml          # Docker Compose configuration file
└── README.md             # This README file
```

## Useful Docker Commands

Here are some helpful commands to manage the Docker environment:

- **Stop all running containers**:

  ```bash
  docker-compose down
  ```

- **Rebuild and restart containers**:

  ```bash
  docker-compose up --build
  ```

- **Check logs for a specific service**:

  ```bash
  docker-compose logs <service-name>
  ```

  For example:

  ```bash
  docker-compose logs api
  ```

- **Access a running container**:

  ```bash
  docker exec -it <container_name> /bin/bash
  ```

  For example, to access the FastAPI API container:

  ```bash
  docker exec -it <api-container-name> /bin/bash
  ```

## Troubleshooting

- **FastAPI server not reachable**: Ensure the FastAPI app is running on `0.0.0.0` and bound to port 8000 (this is handled by the Docker setup).
