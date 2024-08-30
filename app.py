#!/usr/bin/env python3

from aws_cdk import App

# from cicd.pipeline_stack import PipelineStack
from application.application_stack import ApplicationStack
from utils.data_models import load_app_config

app = App()
app_config = load_app_config()

ApplicationStack(
    scope=app,
    construct_id="CDK-Demo-Application",
    app_config=app_config,
)

app.synth()
