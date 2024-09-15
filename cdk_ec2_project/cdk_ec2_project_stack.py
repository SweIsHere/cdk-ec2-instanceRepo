from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput
)
from constructs import Construct

class CdkEc2InstanceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC (puedes usar la default VPC)
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # Security Group
        security_group = ec2.SecurityGroup(self, "InstanceSecurityGroup",
                                           vpc=vpc,
                                           description="Permitir trafico SSH y HTTP desde cualquier lugar",
                                           security_group_name="my-instance-sg"
                                           )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Permitir SSH")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Permitir HTTP")

        instance = ec2.Instance(self, "EC2Instance",
                                instance_name="MV Reemplazar",
                                instance_type=ec2.InstanceType("t2.micro"),
                                machine_image=ec2.MachineImage.generic_linux({
                                    "us-east-1": "ami-0aa28dab1f2852040"  # AMI de Ubuntu
                                }),
                                key_name="vockey",
                                vpc=vpc,
                                security_group=security_group,
                                block_devices=[
                                    ec2.BlockDevice(
                                        device_name="/dev/sda1",
                                        volume=ec2.BlockDeviceVolume.ebs(20)
                                    )
                                ],
                                role=iam.Role.from_role_arn(self, "InstanceRole",
                                                            "arn:aws:iam::724707870327:instance-profile/LabInstanceProfile"),
                                user_data=ec2.UserData.custom('''
                #!/bin/bash
                cd /var/www/html/
                git clone https://github.com/utec-cc-2024-2-test/websimple.git
                git clone https://github.com/utec-cc-2024-2-test/webplantilla.git
                ls -l
            ''')
                                )

        # Outputs
        self.output_instance_id = self.create_output("InstanceId", instance.instance_id)
        self.output_instance_public_ip = self.create_output("InstancePublicIP", instance.instance_public_ip)
        self.output_websimple_url = self.create_output("websimpleURL",
                                                       f"http://{instance.instance_public_ip}/websimple")
        self.output_webplantilla_url = self.create_output("webplantillaURL",
                                                          f"http://{instance.instance_public_ip}/webplantilla")

    def create_output(self, name, value):
        return CfnOutput(self, name, value=value)
