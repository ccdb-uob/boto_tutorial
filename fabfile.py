import sys

import boto3
import logging
from fabric import task

# use loggers right from the start, rather than 'print'
logger = logging.getLogger(__name__)
# this will log boto output to std out
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from dotenv import dotenv_values
config = dotenv_values(".env")

@task
def create(c):
    ec2 = boto3.resource('ec2',
                         region_name='us-east-1',
                         # pass content of config file as named args
                         **config
                         )

    instances = ec2.create_instances(

        ImageId='ami-02e136e904f3da870',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        Placement={
            'AvailabilityZone': 'us-east-1a',
        },

    )
    iid = instances[0].id

    # give the instance a tag name
    ec2.create_tags(
        Resources=[iid],
        Tags=[{'Key': 'Name', 'Value': 'COMSM0072_boto_lab'}]
    )

    logger.info(instances[0])
