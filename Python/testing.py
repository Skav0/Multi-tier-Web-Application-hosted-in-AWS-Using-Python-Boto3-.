import boto3 


client = boto3.client('ec2')




response = client.run_instances(

   

    
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sdh',
            'Ebs': {
                'VolumeSize': 100,
            },
        },
    ],
    ImageId='ami-098e39bafa7e7303d',#put the ami that you want
    InstanceType='t3.micro',
    KeyName='keytest',#put your key
    MaxCount=1,
    MinCount=1,
   

    NetworkInterfaces=[
        {
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'SubnetId': 'subnet-018e2a8e7f0bfe862',    # Must be defined here
            'Groups': ['sg-08e985e6b37a23bd1'],       # Security Group IDs go here
        }],

    UserData='#!/bin/bash\
dnf install -y git\
git clone https://github.com/Skav0/Multi-tier-Web-Application-hosted-in-AWS.git \
dnf install -y httpd\
systemctl start httpd\
systemctl enable httpd\
mkdir /var/www/html/\
mv /Multi-tier-Web-Application-hosted-in-AWS/index.html /var/www/html'
   
)


