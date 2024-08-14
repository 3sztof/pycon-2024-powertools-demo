# api_handler
from typing import Any, Dict
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import Logger, correlation_paths
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.metrics import Metrics
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import Response

from .utils.data_models import LambdaEnv

import boto3
from mypy_boto3_dynamodb import DynamoDBClient

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()
metrics = Metrics()
dynamodb_client: DynamoDBClient = boto3.client("dynamodb")

app = APIGatewayRestResolver()
lambda_env = LambdaEnv()


@app.get("/ping")
@tracer.capture_method
def ping() -> Response:
    return Response(status_code=200, body="pong")


@app.get(rule="/health")
@tracer.capture_method
def health() -> Response:
    return Response(status_code=200, body="OK")


@app.get("/demo/<demo_id>")
@tracer.capture_method
def get_demo_index(demo_id: str) -> Response:  # Value come as str
    return Response(
        status_code=200,
        content_type="text/html",
        body=f"<h1>RequestIndex: {demo_id}</h1>",
    )


@app.get(rule="/feedback")
@tracer.capture_method
def handle_feedback_form_request() -> Response:
    return Response(
        status_code=302,
        headers={
            "Location": lambda_env.feedback_form_url,
        },
    )


@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@tracer.capture_lambda_handler
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> dict:
    # Explicit serialization is no longer needed, this is just for the demo purposes
    api_gateway_event = APIGatewayProxyEvent(data=event)

    response = app.resolve(event=api_gateway_event, context=context)
    return response
