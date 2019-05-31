import string
from base64 import b32encode
from secrets import token_bytes

import troposphere.ec2 as ec2
import troposphere.ssm as ssm
from troposphere import (Base64, FindInMap, GetAtt, Output, Parameter, Ref,
                         Template)


def nextid():
    tb = token_bytes(10)
    tb32 = b32encode(tb)
    tb32s = tb32.decode('utf-8')
    tb32sl = tb32s.lower()
    ni = 'z' + tb32sl
    return ni


t = Template()

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

dhis2_instance = t.add_resource(
    ec2.Instance(
        "DHIS2Instance",
        InstanceType="t3.medium",
        ImageId=Ref(imageid_param),
        KeyName=Ref(keyname_param),
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

print(t.to_json())
