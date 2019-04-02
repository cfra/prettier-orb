.DEFAULT_GOAL := help

DOCKER_COMPOSE_LINT := docker-compose --file .lint/docker-compose.yml

.PHONY: help
help:
	@grep -E '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: prettier
prettier: ## Rewrite all files that are different from Prettier formatting
	$(DOCKER_COMPOSE_LINT) run --rm prettier

