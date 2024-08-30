from aws_cdk import (
    CfnOutput,
    Duration,
    Environment,
    Stack,
    aws_apigateway,
    aws_dynamodb,
    aws_lambda,
    aws_lambda_python_alpha,
    aws_secretsmanager,
)
from constructs import Construct

from utils.data_models import AppConfig


class ApplicationStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        app_config: AppConfig,
        **kwargs,
    ) -> None:
        super().__init__(
            scope=scope,
            id=construct_id,
            env=Environment(
                account=app_config.CDK_DEFAULT_ACCOUNT,
                region=app_config.CDK_DEFAULT_REGION,
            ),
            **kwargs,
        )

        # DynamoDB table - non-relational DB for storing request metadata
        dynamodb_table = aws_dynamodb.Table(
            scope=self,
            id="DynamoDBTable",
            partition_key=aws_dynamodb.Attribute(
                name="RequestID",
                type=aws_dynamodb.AttributeType.STRING,
            ),
        )

        # SecretsManager secret
        some_secret = aws_secretsmanager.Secret(
            scope=self,
            id="SecretString",
        )

        # AWS Lambda function - Serverless backend
        lambda_path = "application/lambda_function"
        lambda_layer = aws_lambda_python_alpha.PythonLayerVersion(
            scope=self,
            id="LambdaLayer",
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_12],
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            entry=lambda_path,
        )
        lambda_function = aws_lambda.Function(
            scope=self,
            id="LambdaFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            code=aws_lambda.Code.from_asset(path=lambda_path),
            handler="app.api_handler.lambda_handler",
            layers=[lambda_layer],
            tracing=aws_lambda.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "INFO",
                "FEEDBACK_FORM_URL": app_config.FEEDBACK_FORM_URL,
                "POWERTOOLS_SERVICE_NAME": "Lambda-Function",
                "POWERTOOLS_METRICS_NAMESPACE": "Lambda-Function",
                "DYNAMODB_TABLE_NAME": dynamodb_table.table_name,
                "SM_SECRET_NAME": some_secret.secret_name,
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        # Grant the Lambda function permissions to access the DynamoDB table
        dynamodb_table.grant_read_write_data(grantee=lambda_function)

        # Grant the Lambda function permissions to access the SecretsManager secret
        some_secret.grant_read(grantee=lambda_function)

        # AWS API Gateway - REST with Lambda proxy integration (high level construct)
        api = aws_apigateway.LambdaRestApi(
            scope=self,
            id="API-Endpoint",
            handler=lambda_function,
        )

        CfnOutput(scope=self, id="FeedbackFormApiUrl", value=f"{api.url}feedback")
        CfnOutput(scope=self, id="PingPongApiUrl", value=f"{api.url}ping")
