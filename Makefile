# Makefile for AI Car Listing Assistant Docker Management
.PHONY: build rebuild up down logs test clean status restart shell help

DOCKER_COMPOSE = docker-compose
SERVICE_NAME = web

# Default target - show help
help:
	@echo "AI Car Listing Assistant Management Commands:"
	@echo "  build     - Build Docker images"
	@echo "  rebuild   - Force rebuild images without cache"
	@echo "  up        - Start containers in detached mode"
	@echo "  down      - Stop and remove containers, networks"
	@echo "  logs      - View container logs (follow)"
	@echo "  test      - Test API endpoint with sample request"
	@echo "  clean     - Remove all Docker artifacts"
	@echo "  status    - Show container status"
	@echo "  restart   - Restart web service"
	@echo "  shell     - Access shell in web container"
	@echo "  help      - Show this help message"

build:
	$(DOCKER_COMPOSE) build

rebuild:
	$(DOCKER_COMPOSE) build --no-cache

up:
	$(DOCKER_COMPOSE) up -d --force-recreate

down:
	$(DOCKER_COMPOSE) down -v

logs:
	$(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)

test:
	@echo "Testing API endpoint..."
	@curl -X POST http://localhost:8000/api/v1/chat \
		-H "Content-Type: application/json" \
		-d '{"session_id": "test_123", "message": "Generate a title for 2020 Honda City with 40,000 km"}' \
		--max-time 10

clean:
	$(DOCKER_COMPOSE) down -v --rmi all
	docker system prune -a --volumes -f

status:
	$(DOCKER_COMPOSE) ps

restart:
	$(DOCKER_COMPOSE) restart $(SERVICE_NAME)

shell:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) bash