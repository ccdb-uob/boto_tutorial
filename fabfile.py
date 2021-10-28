import sys
import time

import boto3
import logging
from fabric import task

# use loggers right from the start, rather than 'print'
logger = logging.getLogger(__name__)
# this will log boto output to std out
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from dotenv import dotenv_values

config = dotenv_values(".env")


@task
def create(c, name='COMSM0072_boto_lab', securitygroup=None):

    ec2 = boto3.resource('ec2',
                         region_name='us-east-1',
                         # pass content of config file as named args
                         **config
                         )

    instances = ec2.create_instances(

        # ImageId='ami-02e136e904f3da870', #(Amazon AMI)
        ImageId='ami-05e4673d4a28889fe',  # (Cloud9 Ubuntu - 2021-10-28T1333)
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.large',
        Placement={
            'AvailabilityZone': 'us-east-1a',
        },
        SecurityGroupIds=[securitygroup] if securitygroup else [],
        KeyName='vockey'

    )
    iid = instances[0].id

    # give the instance a tag name
    ec2.create_tags(
        Resources=[iid],
        Tags=[{'Key': 'Name', 'Value': name}]
    )

    logger.info(instances[0])


@task
def instancedetails(c, name):
    """
    Return an EC2 Instance
    :return:
    """
    ec2 = boto3.resource('ec2', region_name='us-east-1',
                         # pass content of config file as named args
                         **config
                         )
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': [name]},
                 # {'Name': 'instance-state-name', 'Values': ['running']}
                 ])
    # instances is an iterator
    instances = list(instances)

    if len(instances) == 0:
        print('not existing, will create')
        return create(c, name=name)
    else:
        for instance in instances:
            if instance.state['Name'] == "running":
                dns = instance.public_dns_name
                internal_ip = instance.private_ip_address
                public_ip = instance.public_ip_address
                logger.info(
                    f"Instance up and running at {dns} with internal ip {internal_ip}: {public_ip}: {internal_ip}")
            else:
                logger.warning(f"instance {instance.id} not running")
