from pydantic_settings import BaseSettings


class LambdaEnv(BaseSettings):
    LOG_LEVEL: str = "INFO"
    FEEDBACK_FORM_URL: str
    POWERTOOLS_SERVICE_NAME: str
    POWERTOOLS_METRICS_NAMESPACE: str
    DYNAMODB_TABLE_NAME: str
    SM_SECRET_NAME: str
