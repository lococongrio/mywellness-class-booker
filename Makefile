include ./.env

.env:
	cp .env.dist .env

.PHONY: run
run: .env ## run app
	docker compose run --rm python