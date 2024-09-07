import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_ec2_project.cdk_ec2_project_stack import CdkEc2ProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_ec2_project/cdk_ec2_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkEc2ProjectStack(app, "cdk-ec2-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
