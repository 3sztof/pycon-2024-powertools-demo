# AWS CDK & Lambda Powertools Demo

<!-- TOC -->

- [AWS CDK & Lambda Powertools Demo](#aws-cdk--lambda-powertools-demo)
    - [Authors](#authors)
    - [Purpose](#purpose)
    - [Repository Structure](#repository-structure)
    - [Prerequisites](#prerequisites)
    - [Usage](#usage)
        - [CDK Infrastructure Deployment](#cdk-infrastructure-deployment)
        - [Pydantic Application Configuration Validation](#pydantic-application-configuration-validation)

<!-- /TOC -->

## Authors
> Krzysztof Wilczyński & Mateusz Zaremba

TODO: mailto links


## Purpose

TODO: fill in the purpose description

## Repository Structure

| Component                     | Description                                                                                       |
|-------------------------------|---------------------------------------------------------------------------------------------------|
| `pyproject.toml`               | Poetry's configuration file that defines dependencies, scripts, and project metadata.             |
| `poetry.lock`                  | Auto-generated file by Poetry that locks the specific versions of dependencies used in the project. |
| `cdk.json`                     | AWS CDK configuration file that defines how the CDK should execute and deploy the application.    |
| `app.py`                       | The entry point of the CDK application, responsible for instantiating and synthesizing stacks. |
| `application/`                 | Directory containing Python files defining the AWS CDK application stack (`application/application_stack.py`) and application business logic code. |
| `cicd/`                        | Directory containing Python files defining the AWS CDK Pipelines CICD application stack (`cicd/pipeline_stack.py`) responsible for continuous integration and deployment of the CDK stacks in `application/` folder. |
| `README.md`                    | Project documentation, providing an overview, usage instructions, and other relevant information. |
| `.env` (optional)              | Environment file for setting environment variables used by the application, such as AWS credentials. |
| `.env.tpl` (optional)          | Environment file template. Run `cp .env.tpl .env` to create your local `.env` file and fill in the placeholder variable values. |
| `tests/`                       | Directory containing unit and integration tests for the CDK application.                          |
| `.gitignore`                   | Specifies intentionally untracked files to ignore in the Git repository, often including `.env`, `poetry.lock`, and others. |
| `.venv/` (optional)            | Directory containing the virtual environment created by Poetry (if not using a global environment).|
| `cdk.out/`                     | Directory created by the AWS CDK CLI that contains the synthesized CloudFormation templates.      |


## Prerequisites

TODO: 

## Usage

### CDK Infrastructure Deployment

### Pydantic Application Configuration Validation

The demo application utilizes a Pydantic BaseSettings model to automatically load and validate the relevant variables from the shell environment or `.env` file.

If `cdk synth` is called and some of the required variables aren't set either in shell env or the `.env` file, the application will exit, prompting the user to fill in the missing variables.

> Note: you can use the `.env.tpl` template file to create your `.env` file, that will be ignored by `.gitignore`. Just run `cp .env.tpl .env` and fill in the placeholder values in the newly created file.