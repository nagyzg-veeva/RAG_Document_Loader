# Makefile for RAG Document Loader Docker operations

.PHONY: help build run test clean lint compose-up compose-down compose-logs

# Default target
help:
	@echo "Available commands:"
	@echo "  make build        - Build Docker image"
	@echo "  make run          - Run Docker container"
	@echo "  make test         - Run tests in Docker"
	@echo "  make lint         - Run linting in Docker"
	@echo "  make clean        - Remove Docker images and containers"
	@echo "  make compose-up   - Start services with docker-compose"
	@echo "  make compose-down - Stop services with docker-compose"
	@echo "  make compose-logs - View logs from docker-compose"

# Docker commands
build:
	docker build -t rag-document-loader .

run: build
	docker run --rm \
		-e DB_HOST=$${DB_HOST} \
		-e DB_USER=$${DB_USER} \
		-e DB_PASS=$${DB_PASS} \
		-e DB_NAME=$${DB_NAME} \
		-e GCP_PROJECT_ID=$${GCP_PROJECT_ID} \
		-e GCP_LOCATION=$${GCP_LOCATION} \
		-e GCP_CORPUS_NAME=$${GCP_CORPUS_NAME} \
		-v $(PWD)/credentials:/app/credentials:ro \
		-v $(PWD)/config:/app/config:ro \
		-v $(PWD)/plugins:/app/plugins:ro \
		rag-document-loader

test: build
	docker run --rm \
		-e DB_HOST=$${DB_HOST} \
		-e DB_USER=$${DB_USER} \
		-e DB_PASS=$${DB_PASS} \
		-e DB_NAME=$${DB_NAME} \
		-e GCP_PROJECT_ID=$${GCP_PROJECT_ID} \
		-e GCP_LOCATION=$${GCP_LOCATION} \
		-e GCP_CORPUS_NAME=$${GCP_CORPUS_NAME} \
		-v $(PWD)/credentials:/app/credentials:ro \
		-v $(PWD)/config:/app/config:ro \
		-v $(PWD)/plugins:/app/plugins:ro \
		rag-document-loader \
		python -m unittest discover

lint: build
	docker run --rm \
		-v $(PWD):/app \
		rag-document-loader \
		ruff check .

clean:
	docker system prune -f
	docker rmi rag-document-loader 2>/dev/null || true

# Docker Compose commands
compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

compose-logs:
	docker-compose logs -f

# Development commands
dev-shell: build
	docker run --rm -it \
		-e DB_HOST=$${DB_HOST} \
		-e DB_USER=$${DB_USER} \
		-e DB_PASS=$${DB_PASS} \
		-e DB_NAME=$${DB_NAME} \
		-e GCP_PROJECT_ID=$${GCP_PROJECT_ID} \
		-e GCP_LOCATION=$${GCP_LOCATION} \
		-e GCP_CORPUS_NAME=$${GCP_CORPUS_NAME} \
		-v $(PWD)/credentials:/app/credentials:ro \
		-v $(PWD)/config:/app/config:ro \
		-v $(PWD)/plugins:/app/plugins:ro \
		-v $(PWD):/app \
		--entrypoint /bin/bash \
		rag-document-loader

# Quick test
quick-test:
	python test_docker.py