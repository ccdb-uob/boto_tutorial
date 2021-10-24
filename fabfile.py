import boto3
import yaml
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

with open('config.yaml') as f:
    config = yaml.load(f)

from fabric import task


@task
def create(c):
    ec2 = boto3.resource('ec2',
                         aws_access_key_id=config['ACCESS_KEY'],
                         aws_secret_access_key=config['SECRET_KEY'],
                         aws_session_token=config['SESSION_TOKEN'],
                         region_name='us-east-1'
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
    return instances[0]
