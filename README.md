# Boto Demo - Launch AWS EC2

Launch 1 Amazon AMI instance in EC2.
This has been tested with t2.micro instances. 

## Prerequisites

- [ ] python >3.6
- [ ] AWS CLI session secrets

### Setup Python Dependencies

- [ ] create new virtual environment
- [ ] run `pip install -r requirements.txt`

## Configure EC2 instances

- [ ] copy `config.yaml.template` to `config.yaml`
- [ ] edit `config.yaml` and insert your session keys 

run `fab create`

If you don't receive error messages - **Congratulations** You now have a running EC2 instance. Check in the EC2 
concole to confirm.

Stretch goals: 
- [ ] create a second and third fab target that checks the instance state and terminates it. 

 