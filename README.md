# AWS CDK & Lambda Powertools Demo

<!-- TOC -->

- [AWS CDK & Lambda Powertools Demo](#aws-cdk--lambda-powertools-demo)
    - [Introduction](#introduction)
    - [Authors](#authors)
    - [Purpose](#purpose)
    - [Repository Structure](#repository-structure)
    - [Prerequisites](#prerequisites)
    - [Usage](#usage)
        - [CDK Infrastructure Deployment](#cdk-infrastructure-deployment)
        - [Pydantic Application Configuration Validation](#pydantic-application-configuration-validation)
        - [Demo Walkthrough](#demo-walkthrough)
    - [Additional Resources](#additional-resources)

<!-- /TOC -->

## Introduction

This repository hosts the demo code for the PyCon PL 2024 talk "AWS Lambda Powertools and Pydantic - Your Best Friends for Serverless Development". The demo showcases a serverless API built using AWS Lambda, AWS CDK, and various AWS services, with a focus on leveraging the power of AWS Lambda Powertools and Pydantic for improved development practices and best practices in serverless environments.

## Authors

> [Krzysztof Wilczyński](mailto:krzysztof.wilczynski@pm.me) & [Mateusz Zaremba](mailto:matez@orsted.com)

## Purpose

The purpose of this demo is to provide a hands-on example of how AWS Lambda Powertools and Pydantic can simplify and enhance serverless development workflows. The demo application showcases the following key features:

- **AWS CDK Infrastructure**: The AWS infrastructure is deployed using the AWS Cloud Development Kit (CDK), allowing for Infrastructure as Code (IaC) management and easy deployment and teardown of the resources.
- **Pydantic Application Configuration**: The demo application utilizes Pydantic's BaseSettings model to automatically load and validate the relevant environment variables, ensuring a consistent and reliable configuration setup.
- **AWS Lambda Powertools Integration**: The Lambda function in the demo application integrates with AWS Lambda Powertools to generate structured logs, metrics, and distributed tracing, demonstrating how these tools can improve observability and monitoring of serverless applications.

By exploring this demo, you will gain a better understanding of how these powerful tools and practices can be applied to your own serverless development projects, leading to more robust, maintainable, and reliable serverless applications.

## Repository Structure

| Component                     | Description                                                                                       |
|-------------------------------|---------------------------------------------------------------------------------------------------|
| `pyproject.toml`               | Poetry's configuration file that defines dependencies, scripts, and project metadata.             |
| `poetry.lock`                  | Auto-generated file by Poetry that locks the specific versions of dependencies used in the project. |
| `cdk.json`                     | AWS CDK configuration file that defines how the CDK should execute and deploy the application.    |
| `app.py`                       | The entry point of the CDK application, responsible for instantiating and synthesizing stacks. |
| `application/`                 | Directory containing Python files defining the AWS CDK application stack ([`application/application_stack.py`](application/application_stack.py)) and application business logic code. |
| `README.md`                    | Project documentation, providing an overview, usage instructions, and other relevant information. |
| `.env` (optional)              | Environment file for setting environment variables used by the application, such as AWS credentials. |
| `.env.tpl` (optional)          | Environment file template. Run `cp .env.tpl .env` to create your local `.env` file and fill in the placeholder variable values. |
| `.gitignore`                   | Specifies intentionally untracked files to ignore in the Git repository, often including `.env`, `poetry.lock`, and others. |
| `.venv/` (optional)            | Directory containing the virtual environment created by Poetry (if not using a global environment).|
| `cdk.out/` (after running `cdk synth`) | Directory created by the AWS CDK CLI that contains the synthesized CloudFormation templates.      |

## Prerequisites

> Note: you can use our [`makefile`](makefile) to speed up the dependency setup (especially on Debian based GNU/Linux systems), check it out!

1. An [AWS Account](https://signin.aws.amazon.com/signup?request_type=register)
2. AWS CDK (AWS infrastructure deploy / destroy)
    - [NodeJS + npm](https://nodejs.org/en/download/package-manager)
    - [aws-cdk CLI](https://www.npmjs.com/package/aws-cdk) (`npm i -g aws-cdk`)
3. Python
    - [Python 3.11 or newer + pip](https://www.python.org/downloads/) 
    - [Python Poetry](https://pypi.org/project/poetry/) (`pip install poetry`)
4. Docker, or other CDK-compatible container runtime (used to build and package Lambda functions before deployment)

## Usage

### CDK Infrastructure Deployment

1. Deploy the AWS resources:
   - `cdk deploy` (or `make deploy`)
   - Note down the API URL(s) from the deployment output
2. Destroy the AWS resources:
   - `cdk destroy` (or `make destroy`)
3. Diff the AWS resource changes (if you make local CDK changes):
   - `cdk diff`

### Pydantic Application Configuration Validation

The demo application utilizes a Pydantic `BaseSettings` model to automatically load and validate the relevant variables from the shell environment or `.env` file. If `cdk synth` is called and some of the required variables aren't set, the application will exit, prompting the user to fill in the missing variables.

You can use the `.env.tpl` template file to create your `.env` file, which will be ignored by `.gitignore`. Just run `cp .env.tpl .env` and fill in the placeholder values in the newly created file.

### Demo Walkthrough

1. Install the dependencies, deploy the AWS CDK application into your AWS account
1. Send some requests towards the deployed API endpoints / resources (URLs outputted after deploying CDK resources)
1. Analyze the API resolver/handler Lambda function code [`application/lambda_function/app/api_handler.py`](application/lambda_function/app/api_handler.py)
1. In the AWS console:
   - Navigate to CloudWatch
   - Check out the generated Lambda function logs, metrics, and X-Ray traces.
1. Customize the demo to fit your needs or explore further:
   - Modify the infrastructure or application code
   - Test your ideas
   - Explore more advanced Powertools and Pydantic features
   - If you find something cool that should be a part of this demo codebase, raise a PR!

## Additional Resources

The following resources provide further information on the key technologies and services used in this demo:

1. **AWS Lambda Powertools**
   - Official Documentation: [https://awslabs.github.io/aws-lambda-powertools-python/](https://awslabs.github.io/aws-lambda-powertools-python/)
   - GitHub Repository: [https://github.com/awslabs/aws-lambda-powertools-python](https://github.com/awslabs/aws-lambda-powertools-python)
   - AWS Blog Post: [https://aws.amazon.com/blogs/opensource/simplifying-serverless-best-practices-with-lambda-powertools/](https://aws.amazon.com/blogs/opensource/simplifying-serverless-best-practices-with-lambda-powertools/)

2. **Pydantic**
   - Official Documentation: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
   - GitHub Repository: [https://github.com/pydantic/pydantic](https://github.com/pydantic/pydantic)
   - Real Python Tutorial: [https://realpython.com/pydantic-python/](https://realpython.com/pydantic-python/)

3. **AWS Lambda**
   - AWS Lambda Developer Guide: [https://docs.aws.amazon.com/lambda/latest/dg/welcome.html](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
   - AWS Lambda FAQs: [https://aws.amazon.com/lambda/faqs/](https://aws.amazon.com/lambda/faqs/)

4. **Amazon API Gateway**
   - API Gateway Developer Guide: [https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
   - API Gateway FAQs: [https://aws.amazon.com/api-gateway/faqs/](https://aws.amazon.com/api-gateway/faqs/)

5. **AWS AppSync**
   - AppSync Developer Guide: [https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html](https://docs.aws.amazon.com/appsync/latest/devguide/