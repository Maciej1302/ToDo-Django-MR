build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

restart: down up

supercode:
	isort .
	black .
	flake8 .
	mypy .

