#!/usr/bin/env python3

from aws_cdk import App, Environment
import os

# from cicd.pipeline_stack import PipelineStack
from application.application_stack import ApplicationStack
# from .utils import load_config

# config = load_config()
ENABLE_PIPELINE = False

app = App()

if ENABLE_PIPELINE:
    pass
    # PipelineStack(
    #     scope=app,
    #     construct_id="CDK-Demo-Pipeline",
    #     env=Environment(
    #         account=os.environ["CDK_DEFAULT_ACCOUNT"],
    #         region=os.environ["CDK_DEFAULT_REGION"],
    #     ),
    #     # config=config,
    # )
else:
    ApplicationStack(
        scope=app,
        construct_id="CDK-Demo-Application",
        env=Environment(
            account=os.environ["CDK_DEFAULT_ACCOUNT"],
            region=os.environ["CDK_DEFAULT_REGION"],
        ),
        # config=config,
    )

app.synth()
