from aws_cdk import Stage, Environment, Stack, CfnParameter
from constructs import Construct

from application.application_stack import ApplicationStack


class DeployAppStage(Stage):
    def __init__(
        self,
        scope: Construct,
        id: str,
        env: Environment,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        ApplicationStack(
            scope=self,
            construct_id="Demo-Application-Stack",
            env=env,
        )


class PipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: Environment,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)

        self.github_repository = "3sztof/virtual-coffee"

        # Github access token CloudFormation parameter
        # Created on Github, should include permissions for:
        # * repo * admin:repo_hook
        github_token_parameter = CfnParameter(
            self, "GithubTokenParameter", no_echo=True
        )

        # Set up a secret required by CodePipeline's Github webhook
        self.github_token = SecretValue.cfn_parameter(github_token_parameter)
        secretsmanager.Secret(
            self, "GithubTokenSecret", secret_string_value=self.github_token
        )

        pipeline_name = pipeline_config.pipeline_name

        # TODO: add alternative repository configuration options

        # Prepare pipeline engine agnostic synth step definition
        synth_step = pipelines.ShellStep(
            id=f"SynthStep-{pipeline_name}",
            input=pipelines.CodePipelineSource.git_hub(
                repo_string=self.github_repository,
                branch=pipeline_config.branch_name,
                authentication=self.github_token,
            ),
            env={"CDK_NOTICES": "false"},
            install_commands=[
                "pip install poetry",
                "cd src",
                "poetry export -f requirements.txt -o requirements.txt --without-hashes",
                "pip install -r requirements.txt",
                # "npm install -g aws-cdk@latest",
            ],
            commands=[
                # TODO prio 3 add mypy and pytest unit tests
                "npx aws-cdk synth --no-notices"
            ],
            primary_output_directory="src/cdk.out",
        )

        # Define a CodePipeline
        pipeline = pipelines.CodePipeline(
            self,
            f"CodePipeline-{pipeline_name}",
            pipeline_name=f"VirtualCoffePipeline-{pipeline_name}",
            self_mutation=True,
            docker_enabled_for_synth=True,
            # synth_code_build_defaults=pipelines.CodeBuildOptions(
            #     build_environment=codebuild.BuildEnvironment(
            #         build_image=codebuild.LinuxBuildImage.STANDARD_7_0
            #     )
            # ),
            synth=synth_step,
        )

        # Deploy shared infrastructure (such as SNS for maintainers, SES, Route53)
        pipeline.add_stage(
            DeploySharedStage(
                self,
                f"VirtualCoffee-Shared-{pipeline_name}",
                env=pipeline_config.target_environment,
                global_config=self.global_config,
            )
        )

        # Conditionally enable manual approval step
        pre_steps = []
        if pipeline_name.lower() != "test":
            pre_steps.append(pipelines.ManualApprovalStep("ManualApproval"))

        # Set up paralel deployment wave with manual approval
        prod_deployment_wave = pipeline.add_wave(
            f"DeploymentWave-{pipeline_name}", pre=pre_steps
        )

        for workspace in pipeline_config.deploy_workspaces:
            prod_deployment_wave.add_stage(
                DeployAppStage(
                    self,
                    f"VirtualCoffee-{workspace.workspace_name}-{pipeline_name}",
                    env=pipeline_config.target_environment,
                    global_config=self.global_config,
                    workspace_config=workspace,
                )
            )

        for pipeline_config in pipeline_configs:
            self.create_pipeline(pipeline_config)

    def create_pipeline(
        self, pipeline_config: PipelineConfig
    ) -> pipelines.CodePipeline:
        
