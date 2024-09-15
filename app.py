# app.py
import aws_cdk as cdk
from lib.cdk_ec2_instance_stack import CdkEc2InstanceStack

app = cdk.App()
#.*-
CdkEc2InstanceStack(app, "CdkEc2InstanceStack",
                    env=cdk.Environment(account="724707870327", region="us-east-1")
                    )

app.synth()
