DOCKER_COMPOSE_RUN_CDK=docker compose run --rm cdk
DOCKER_COMPOSE_RUN_PYTHON=docker compose run --rm python
include ./.env

.env:
	cp .env.dist .env

.PHONY: run
run: .env ## run app
	$(DOCKER_COMPOSE_RUN_PYTHON) bash -c "python index.py"
.PHONY: remove-image
remove-image: ## remove python image
	docker rmi mywellness-class-booker-python

### CDK ###
.PHONY: cdk-install
cdk-install: ## Install dependencies
	$(DOCKER_COMPOSE_RUN_CDK) npm install

.PHONY: cdk-update
cdk-update: ## Update dependencies
	$(DOCKER_COMPOSE_RUN_CDK) npm update

.PHONY: cdk-lint
cdk-lint: ## Run eslint
	$(DOCKER_COMPOSE_RUN_CDK) npm run lint

.PHONY: cdk-prettier
cdk-prettier: ## Run prettier
	$(DOCKER_COMPOSE_RUN_CDK) npm run prettier

.PHONY: cdk-diff
cdk-diff: cdk-build-python-layer ## Shows the diff of the changes you have with what is deployed
	$(DOCKER_COMPOSE_RUN_CDK) npm run cdk-diff -- --profile PersonalAdmin

.PHONY: cdk-synth
cdk-synth: cdk-build-python-layer ## Synthesize the cloudformation template from the CDK code
	$(DOCKER_COMPOSE_RUN_CDK) npm run cdk-synth -- --profile PersonalAdmin

.PHONY: cdk-deploy
cdk-deploy: cdk-build-python-layer ## Deploy all stacks
	$(DOCKER_COMPOSE_RUN_CDK) npm run cdk-deploy -- --profile PersonalAdmin

.PHONY: cdk-build-python-layer
cdk-build-python-layer: ## Build python layer
	$(DOCKER_COMPOSE_RUN_PYTHON) rm -rf /src/layer \
	&& $(DOCKER_COMPOSE_RUN_PYTHON) mkdir -p /src/layer/python \
	&& $(DOCKER_COMPOSE_RUN_PYTHON) pip install -r /src/requirements.txt -t /src/layer/python/