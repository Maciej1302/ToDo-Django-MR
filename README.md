
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

### 2. First-time Setup - Initial Application Launch Instructions (TODO-Django-MR)

To set up and launch the application for the first time, follow these steps:

1. **Create a .env file** in the application directory and add your Django secret key:
    ```
    SECRET_KEY=your_secret_key_here
    ```
   
2. **Build the Docker container** by running:
    ```bash
    make build
    ```

3. **Start the application** on port `http://0.0.0.0:8000/` by running:
    ```bash
    make up
    ```

4. **Run database migrations** to set up the initial database schema:
    ```bash
    docker compose exec web python3 manage.py migrate
    ```

5. **Create a superuser** to access the admin panel and manage application users:
    ```bash
    docker compose exec web python3 manage.py createsuperuser
    ```
    Follow the prompts to set up an admin username and password.

### 3. Accessing the Application

Once the container is running, you can access the application by navigating to:

http://0.0.0.0:8000/todo/api/token/ to obtain refresh and access token

http://0.0.0.0:8000/todo/api/token/refresh to refresh access token

http://0.0.0.0:8000/todo/tasks to list tasks or create task

http://0.0.0.0:8000/todo/task/{pk} to retrieve/update/destroy task

http://0.0.0.0:8000/todo/cases to list cases or create case

http://0.0.0.0:8000/todo/case/{pk} to retrieve/update/destroy case




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

Dependencies are listed in requirements.txt and include:

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
