
# Todo Django Application

This project is a Django application with a REST API using Django REST Framework (DRF) and JWT authentication. The application is containerized using Docker for ease of deployment and development.

## Requirements

- **Docker** and **Docker Compose**: To build and run the application in isolated containers.

## Setup and Installation

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Build and run the application

You can build and start the application using Docker Compose:

```bash
make build
make up
```

This will:
- Build the Docker image as specified in the Dockerfile.
- Start the Django development server on http://localhost:8000.

> **Note:** The server is configured to run on port 8000. If this port is already in use, you may need to modify the port mapping in the `docker-compose.yml` file.

### 3. Accessing the Application

Once the container is running, you can access the application by navigating to:

http://localhost:8000

### 4. Running Tests

To run tests for the application, you can use the following command:

```bash
make test
```

### 5. Code Quality

This project includes dependencies for code quality checks. You can run these checks using the following command:


```bash
make supercode
```

## Project Structure

- **docker-compose.yml**: Defines services, volumes, and ports for the Docker setup.
- **Dockerfile**: Defines the Docker image setup for the Django application.
- **requirements.txt**: Lists all Python dependencies required by the application, including Django and code quality tools.

## Dependencies

Dependencies are listed in `requirements.txt` and include:

- **Django 5.1.2** - The web framework.
- **Django REST Framework 3.14.0** - A toolkit for building Web APIs.
- **Django REST Framework Simple JWT 5.3.1** - For JWT-based authentication.

### Development Dependencies

- **Black**: Code formatter.
- **Flake8**: Code style enforcer.
- **Isort**: Import sorter.

## Authentication

The application uses JWT (JSON Web Token) authentication provided by **Django REST Framework Simple JWT**. This ensures secure token-based authentication for users accessing the API.

## Views and API

The REST API in this application is structured using **Django REST Framework’s Generic Class-Based Views**. This setup provides a streamlined way to create CRUD (Create, Read, Update, Delete) functionality for the API endpoints with minimal code while following DRF’s best practices.

## Database

The application uses a SQLite database, which is saved as `db.sqlite3` in the project directory. The database file is mapped to persist data even when the container restarts.