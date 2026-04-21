import boto3
#**************************creating a vpc.*****************************************
client = boto3.client('ec2')

rvpc = client.create_vpc(
    CidrBlock='192.168.0.0/16',
)





#**********************subnets************************************************



#After creating the vpc, i used the vpc id in the subnets below, and i included the zones where i can create the subnets.


subnets=[{'az':'us-east-1a','cidr':'192.168.10.0/24'},
         {'az':'us-east-1a','cidr':'192.168.20.0/24'},
         {'az':'us-east-1b','cidr':'192.168.30.0/24'},
         {'az':'us-east-1b','cidr':'192.168.40.0/24'}
         
         
         ]

l=[]
for i in subnets:
    response = client.create_subnet(
        AvailabilityZone=i['az'],
        CidrBlock=i['cidr'],
        VpcId=rvpc['Vpc']['VpcId'],)
    l.append(response['Subnet']['SubnetId'])


#**********************************************************************



#**********************security groups************************************************




rsg1 = client.create_security_group(
    Description='Public SG',
    GroupName='Public SG',
    VpcId=rvpc['Vpc']['VpcId'],
)

rsg2 = client.create_security_group(
    Description='Private SG',
    GroupName='Private SG',
    VpcId=rvpc['Vpc']['VpcId'],
)

#**********************************************************************







#**********************routing tables************************************************




response = client.create_route_table(
    VpcId=rvpc['Vpc']['VpcId'],
)
response = client.create_route_table(
    VpcId=rvpc['Vpc']['VpcId'],
)


#**********************************************************************




#**********************NAT GWs************************************************

#*****creating EIPs for the NAT GWs***

reip1 = client.allocate_address(
    Domain='vpc',
)
reip2 = client.allocate_address(
    Domain='vpc',
)
#******************************



response = client.create_nat_gateway(
    AllocationId=reip1['AllocationId'],
    SubnetId=l[0],
)

response = client.create_nat_gateway(
    AllocationId=reip2['AllocationId'],
    SubnetId=l[1],
)


#**********************************************************************

#**********************EC2 insatnces**********************************

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
    SecurityGroupIds=[
        rsg1['GroupId'],
    ],
    SubnetId=l[0],
   
)

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
    SecurityGroupIds=[
        rsg2['GroupId'],
    ],
    SubnetId=l[1],
    UserData='#!/bin/bash\
dnf install -y git\
git clone https://github.com/Skav0/Multi-tier-Web-Application-hosted-in-AWS.git \
dnf install -y httpd\
systemctl start httpd\
systemctl enable httpd\
mkdir /var/www/html/\
mv /Multi-tier-Web-Application-hosted-in-AWS/index.html /var/www/html'
   
)




##########################################################################################



#*************************ALB**************************************

client = boto3.client('elb')



ralb1 = client.create_load_balancer(
    Listeners=[
        {
            'InstancePort': 80,
            'InstanceProtocol': 'HTTP',
            'LoadBalancerPort': 80,
            'Protocol': 'HTTP',
        },
    ],
    LoadBalancerName='alb1',
    SecurityGroups=[
        rsg1['GroupId'],
    ],
    Subnets=[
        l[0],
    ],
)

ralb2 = client.create_load_balancer(
    Listeners=[
        {
            'InstancePort': 80,
            'InstanceProtocol': 'HTTP',
            'LoadBalancerPort': 80,
            'Protocol': 'HTTP',
        },
    ],
    LoadBalancerName='alb2',
    SecurityGroups=[
        rsg2['GroupId'],
    ],
    Subnets=[
        l[1],
    ],
)
