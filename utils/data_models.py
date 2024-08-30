import re

from pydantic import SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    FEEDBACK_FORM_URL: str
    CDK_DEFAULT_REGION: str
    CDK_DEFAULT_ACCOUNT: str
    DEMO_SECRET_VALUE: SecretStr

    @field_validator("CDK_DEFAULT_REGION")
    def validate_region(cls, v):
        valid_regions = [
            "us-east-1",
            "us-west-1",
            "us-west-2",
            "eu-west-1",
            "eu-west-2",
            "eu-west-3",
            "eu-central-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "ap-northeast-2",
            "sa-east-1",
            "ca-central-1",
        ]
        if v not in valid_regions:
            raise ValueError(f"'{v}' is not a valid AWS region.")
        return v

    @field_validator("CDK_DEFAULT_ACCOUNT")
    def validate_account(cls, v):
        if not re.match(pattern=r"^\d{12}$", string=v):
            raise ValueError("AWS Account ID must be a 12-digit number.")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True
        env_prefix = ""  # Set if needed


def load_app_config() -> AppConfig:
    """Load the AppConfig object or catch validation errors and identify missing variables

    Returns:
        AppConfig: The loaded AppConfig object
    """

    try:
        return AppConfig()

    except ValidationError as e:
        print("The following environment variables are misconfigured:")
        for error in e.errors():
            print(f"- {error['loc'][0].upper()} ({error['msg']})")

        exit(code=1)
