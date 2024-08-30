import json
from typing import Any, Dict

import boto3
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.logging import Logger, correlation_paths
from aws_lambda_powertools.metrics import Metrics, MetricUnit
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.typing import LambdaContext
from mypy_boto3_dynamodb import DynamoDBClient

from .utils.data_models import LambdaEnv

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()
metrics = Metrics()

dynamodb_client: DynamoDBClient = boto3.client("dynamodb")

app = APIGatewayRestResolver()
lambda_env = LambdaEnv()


# Simple ping-pong api endpoint, count invocations in CloudWatch metrics
@app.get("/ping")
def ping() -> Response:
    metrics.add_metric(name="PingPongInvocations", unit=MetricUnit.Count, value=1)
    return Response(
        status_code=200,
        content_type=content_types.TEXT_HTML,
        body="<h1>Pong</h1>",
    )


# Example of resource id handling in Powertools proxy integration router
@app.get("/demo/<demo_id>")
@tracer.capture_method
def get_demo_index(demo_id: str) -> Response:
    return Response(
        status_code=200,
        content_type=content_types.TEXT_HTML,
        body=f"<h1>RequestIndex: {demo_id}</h1>",
    )


# Main demo - count /feedback resource invocation # TODO: comment
@app.get(rule="/feedback")
@tracer.capture_method
def handle_feedback_form_request() -> Response:
    # Custom metric - count API invocations
    metrics.add_metric(name="FeedbackFormInvocations", unit=MetricUnit.Count, value=1)

    # Get some secret from SecretsManager
    some_secret = parameters.get_secret(
        name=lambda_env.SM_SECRET_NAME,
        max_age=300,
    )

    # Save request headers in DynamoDB table
    table_name = lambda_env.DYNAMODB_TABLE_NAME
    headers = app.current_event.headers
    dynamodb_client.put_item(
        TableName=table_name,
        Item={
            "RequestID": {"S": app.lambda_context.aws_request_id},
            "Headers": {"S": json.dumps({str(k): str(v) for k, v in headers.items()})},
            "SomeSecret": {"S": some_secret},
        },
    )

    return Response(
        status_code=302,
        headers={
            "Location": lambda_env.FEEDBACK_FORM_URL,
        },
    )


@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST,
    log_event=True,
)
@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> dict:
    return app.resolve(event=event, context=context)
