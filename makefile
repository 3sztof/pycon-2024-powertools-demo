# Set the CDK app name
APPLICATION_STACK_NAME ?= CDK-Demo-Application

# Intall Poetry, activate Poetry venv, install dependencies
install-pydeps:
	@pip install poetry
	@poetry shell
	@poetry install

install-cdk:
	@sudo apt-get update
	@sudo apt-get install -y nodejs npm
	@sudo npm install -g aws-cdk@latest


# CDK Deploy command
deploy:
	@poetry run cdk deploy $(APPLICATION_STACK_NAME)

# Ruff linting command
lint:
	@poetry run ruff check --select I --fix
	@poetry run ruff format .

# Run static checks / tests
check-static:
	@poetry run mypy .

# Check dependencies security
check-security:
	@poetry run bandit -r -c pyproject.toml .

# Run both deploy and lint
all: lint check-static check-security deploy
