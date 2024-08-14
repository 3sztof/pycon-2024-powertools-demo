from aws_cdk import (
    Stack,
    Environment,
    aws_lambda,
    aws_apigateway,
    aws_lambda_python_alpha,
    aws_dynamodb,
    CfnOutput,
)
from constructs import Construct


FEEDBACK_FORM_URL = "https://pulse.aws/survey/RXQDDT5T"


class ApplicationStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: Environment,
        **kwargs,
    ) -> None:
        super().__init__(scope, id=construct_id, env=env, **kwargs)

        # DynamoDB table - non-relational DB for storing request metadata
        dynamodb_table = aws_dynamodb.Table(
            scope=self,
            id="DynamoDB-Table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING,
            ),
        )

        # AWS Lambda function - Serverless backend
        lambda_path = "application/lambda_function"
        lambda_layer = aws_lambda_python_alpha.PythonLayerVersion(
            scope=self,
            id="Lambda-Layer",
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_12],
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            entry=lambda_path,
        )
        lambda_function = aws_lambda.Function(
            scope=self,
            id="Lambda-Function",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            code=aws_lambda.Code.from_asset(path=lambda_path),
            handler="app.api_handler.lambda_handler",
            layers=[lambda_layer],
            tracing=aws_lambda.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "INFO",
                "FEEDBACK_FORM_URL": FEEDBACK_FORM_URL,
                "POWERTOOLS_SERVICE_NAME": "Lambda-Function",
                "POWERTOOLS_METRICS_NAMESPACE": "Lambda-Function",
                "DYNAMODB_TABLE_NAME": dynamodb_table.table_name,
            },
        )

        # AWS API Gateway - REST with Lambda proxy integration (high level construct)
        api = aws_apigateway.LambdaRestApi(
            scope=self,
            id="API-Endpoint",
            handler=lambda_function,
        )

        CfnOutput(self, "FeedbackFormApiUrl", value=f"{api.url}/feedback")
