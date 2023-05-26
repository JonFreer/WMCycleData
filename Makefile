ifeq ($(INFRA), dev)
FILES=-f docker-compose.yaml -f docker-compose.dev.yaml
else
FILES=-f docker-compose.yaml
endif

.PHONY: all
all: up

.PHONY: up down build pull logs
up:
	docker-compose $(FILES) up
down:
	docker-compose $(FILES) down --remove-orphans
build:
	docker-compose $(FILES) build
pull:
	docker-compose $(FILES) pull
logs:
	docker-compose $(FILES) logs