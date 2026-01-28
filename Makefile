.PHONY: help build up down logs test test-backend test-frontend

help:
	@echo "Insights App - Available Commands"
	@echo "=================================="
	@echo "make build              - Build Docker images"
	@echo "make up                 - Start containers"
	@echo "make down               - Stop containers"
	@echo "make logs               - View container logs"
	@echo "make logs-backend       - View backend logs only"
	@echo "make logs-frontend      - View frontend logs only"
	@echo "make test               - Run all tests"
	@echo "make test-backend       - Run backend tests"
	@echo "make test-frontend      - Run frontend tests"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

test: test-backend test-frontend

test-backend:
	@echo "Running backend tests..."
	./.venv/bin/python -m pytest backend/tests/ -v --tb=short

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test -- --run

