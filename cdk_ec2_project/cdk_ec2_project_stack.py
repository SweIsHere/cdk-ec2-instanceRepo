from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam
)


class Ec2WebStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Parámetros definidos
        instance_name = core.CfnParameter(self, "InstanceName",
                                          type="String",
                                          default="MV Reemplazar",
                                          description="Nombre de la instancia a crear")

        ami_id = core.CfnParameter(self, "AMI",
                                   type="String",
                                   default="ami-0aa28dab1f2852040",
                                   description="ID de la AMI")

        # Crear el Security Group
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        security_group = ec2.SecurityGroup(self, "InstanceSecurityGroup",
                                           vpc=vpc,
                                           description="Permitir tráfico SSH y HTTP desde cualquier lugar")

        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Permitir SSH")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Permitir HTTP")

        # Asociar el Instance Profile a la instancia EC2
        instance = ec2.Instance(self, "EC2Instance",
                                instance_type=ec2.InstanceType("t2.micro"),
                                machine_image=ec2.MachineImage.generic_linux({
                                    "us-east-1": ami_id.value_as_string
                                }),
                                vpc=vpc,
                                key_name="vockey",
                                security_group=security_group,
                                block_devices=[
                                    ec2.BlockDevice(
                                        device_name="/dev/sda1",
                                        volume=ec2.BlockDeviceVolume.ebs(20)
                                    )
                                ],
                                # Aquí se usa el Instance Profile en lugar del rol directamente
                                role=iam.InstanceProfile.from_instance_profile_arn(self, "InstanceProfile",
                                                                                    "arn:aws:iam::724707870327:instance-profile/LabInstanceProfile"),
                                user_data=ec2.UserData.custom('''
                                    #!/bin/bash
                                    cd /var/www/html/
                                    git clone https://github.com/utec-cc-2024-2-test/websimple.git
                                    git clone https://github.com/utec-cc-2024-2-test/webplantilla.git
                                    ls -l
                                ''')
                                )

        # Salidas del stack
        core.CfnOutput(self, "InstanceId",
                       description="ID de la instancia EC2",
                       value=instance.instance_id)

        core.CfnOutput(self, "InstancePublicIP",
                       description="IP pública de la instancia",
                       value=instance.instance_public_ip)

        core.CfnOutput(self, "WebSimpleURL",
                       description="URL de websimple",
                       value=f"http://{instance.instance_public_ip}/websimple")

        core.CfnOutput(self, "WebPlantillaURL",
                       description="URL de webplantilla",
                       value=f"http://{instance.instance_public_ip}/webplantilla")
