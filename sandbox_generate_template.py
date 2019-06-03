from base64 import b32encode
from secrets import token_bytes

import troposphere.ec2 as ec2
import troposphere.ssm as ssm
from troposphere import (Base64, FindInMap, GetAtt, Output, Parameter, Ref,
                         Tags, Template)


def nextid():
    tb = token_bytes(10)
    tb32 = b32encode(tb)
    tb32s = tb32.decode('utf-8')
    tb32sl = tb32s.lower()
    ni = 'z' + tb32sl
    return ni


class AdHocTemplate(Template):
    def r(self, resource_type_class, **kwargs):
        title = resource_type_class.__name__.lower()
        resource = resource_type_class(title, **kwargs)
        return self.add_resource(resource)


NAME = 'dhis2-sandbox'
SECURITY_GROUP_NAME = NAME
INSTANCE_TAG_NAME = NAME


t = AdHocTemplate()

keyname_param = t.add_parameter(
    Parameter(
        "KeyName",
        Description="Name of an existing EC2 KeyPair to enable SSH access to the instance",
        Type="AWS::EC2::KeyPair::KeyName",
    )
)

imageid_param = t.add_parameter(
    Parameter(
        "ImageId",
        Description="ID of AMI for instance",
        Type="AWS::EC2::Image::Id",
    )
)

elastic_ip = t.r(
    ec2.EIP,
    Domain='vpc',
)


dhis2_instance = t.add_resource(
    ec2.Instance(
        "DHIS2Instance",

        # AdditionalInfo="",
        # Affinity="",
        # AvailabilityZone="",
        BlockDeviceMappings=[
            ec2.BlockDeviceMapping(
                "BlockDeviceMapping",
                DeviceName="/dev/sda1",
                Ebs=ec2.EBSBlockDevice(
                    "BootVolume",
                    VolumeSize="16",
                ),
            ),
        ],
        # CreditSpecification={},
        # DisableApiTermination=False,
        # EbsOptimized=False,
        # ElasticGpuSpecifications=[],
        # ElasticInferenceAccelerators=[],
        # HostId="",
        # IamInstanceProfile="",
        ImageId=Ref(imageid_param),
        # InstanceInitiatedShutdownBehavior="",
        InstanceType="t3.medium",
        # Ipv6AddressCount=0,
        # Ipv6Addresses=[],
        # KernelId="",
        KeyName=Ref(keyname_param),
        # LaunchTemplate={},
        # LicenseSpecifications=[],
        # Monitoring=False,
        # NetworkInterfaces=[],
        # PlacementGroupName="",
        # PrivateIpAddress="",
        # RamdiskId="",
        # SecurityGroupIds=[],
        SecurityGroups=[
            SECURITY_GROUP_NAME,
        ],
        # SourceDestCheck=False,
        # SsmAssociations=[],
        # SubnetId="",
        Tags=Tags(
            Name=INSTANCE_TAG_NAME,
        ),
        # Tenancy="",
        # UserData="",
        # Volumes=[],

    )
)

t.add_output(
    [
        Output(
            "InstanceId",
            Description="InstanceId of the newly created EC2 instance",
            Value=Ref(dhis2_instance),
        ),
        Output(
            "AZ",
            Description="Availability Zone of the newly created EC2 instance",
            Value=GetAtt(dhis2_instance, "AvailabilityZone"),
        ),
        Output(
            "PublicIP",
            Description="Public IP address of the newly created EC2 instance",
            Value=GetAtt(dhis2_instance, "PublicIp"),
        ),
        Output(
            "PrivateIP",
            Description="Private IP address of the newly created EC2 instance",
            Value=GetAtt(dhis2_instance, "PrivateIp"),
        ),
        Output(
            "PublicDNS",
            Description="Public DNSName of the newly created EC2 instance",
            Value=GetAtt(dhis2_instance, "PublicDnsName"),
        ),
        Output(
            "PrivateDNS",
            Description="Private DNSName of the newly created EC2 instance",
            Value=GetAtt(dhis2_instance, "PrivateDnsName"),
        ),
    ]
)

if __name__ == '__main__':
    print(t.to_json())
