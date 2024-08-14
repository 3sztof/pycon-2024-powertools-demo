# import aws_cdk as core
# import aws_cdk.assertions as assertions

# from pt_cdk_demo.pt_cdk_demo_stack import PtCdkDemoStack

# # example tests. To run these tests, uncomment this file along with the example
# # resource in pt_cdk_demo/pt_cdk_demo_stack.py
# def test_sqs_queue_created():
#     app = core.App()
#     stack = PtCdkDemoStack(app, "pt-cdk-demo")
#     template = assertions.Template.from_stack(stack)

# #     template.has_resource_properties("AWS::SQS::Queue", {
# #         "VisibilityTimeout": 300
# #     })
