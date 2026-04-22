import boto3

#**************************creating a vpc.*****************************************
client = boto3.client('ec2')

rvpc = client.create_vpc(
    CidrBlock='192.168.0.0/16',
)





#**********************subnets************************************************



#After creating the vpc, i used the vpc id in the subnets below, and i included the zones where i can create the subnets.


subnets=[{'az':'us-east-1b','cidr':'192.168.10.0/24'},
         {'az':'us-east-1a','cidr':'192.168.20.0/24'},
         {'az':'us-east-1b','cidr':'192.168.30.0/24'},
         {'az':'us-east-1a','cidr':'192.168.40.0/24'}
         
         
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

#create an internet gateway:

igwrep = client.create_internet_gateway(
)

client.attach_internet_gateway(
    InternetGatewayId=igwrep['InternetGateway']['InternetGatewayId'],
      VpcId=rvpc['Vpc']['VpcId'])

#public route table
rtrep1 = client.create_route_table(
    VpcId=rvpc['Vpc']['VpcId'],
)

#private route table1
rtrep2 = client.create_route_table(
    VpcId=rvpc['Vpc']['VpcId'],
)
#private route table2
rtrep3 = client.create_route_table(
    VpcId=rvpc['Vpc']['VpcId'],
)

#creating routes for the route tables:
#internet route
response = client.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igwrep['InternetGateway']['InternetGatewayId'],
    RouteTableId=rtrep1['RouteTable']['RouteTableId'],
)




#**********************NAT GWs************************************************

#*****creating EIPs for the NAT GWs***
reip1 = client.allocate_address(
    Domain='vpc',
)
reip2 = client.allocate_address(
    Domain='vpc',
)
#******************************
#creating the NAT GWs
rnatgw1 = client.create_nat_gateway(
    AllocationId=reip1['AllocationId'],
    SubnetId=l[2],
)
rnatgw2 = client.create_nat_gateway(
    AllocationId=reip2['AllocationId'],
    SubnetId=l[3],
)
nat_gw_ids = [
    rnatgw1['NatGateway']['NatGatewayId'],
    rnatgw2['NatGateway']['NatGatewayId']
]

print("Waiting for NAT Gateways to become available... (This usually takes 2-3 minutes)")
waiter = client.get_waiter('nat_gateway_available')
waiter.wait(
    NatGatewayIds=nat_gw_ids,
    WaiterConfig={'Delay': 15, 'MaxAttempts': 40}
)
print("NAT Gateways are ready! Proceeding to routing...")
#**********************************************************************









#nat gw route(for the 2 private rts)
response = client.create_route(
    DestinationCidrBlock='0.0.0.0/0',
        NatGatewayId=rnatgw1['NatGateway']['NatGatewayId'],

    RouteTableId=rtrep2['RouteTable']['RouteTableId'],
)

response = client.create_route(
    DestinationCidrBlock='0.0.0.0/0',
        NatGatewayId=rnatgw2['NatGateway']['NatGatewayId'],

    RouteTableId=rtrep3['RouteTable']['RouteTableId'],
)



#route table association with subnets
#public association(1rt-->2subnets).
response = client.associate_route_table(
    RouteTableId=rtrep1['RouteTable']['RouteTableId'],
    SubnetId=l[2],
)
response = client.associate_route_table(
    RouteTableId=rtrep1['RouteTable']['RouteTableId'],
    SubnetId=l[3],
)
#private association(1rt---->2subnets).
response = client.associate_route_table(
    RouteTableId=rtrep2['RouteTable']['RouteTableId'],
    SubnetId=l[0],
)
response = client.associate_route_table(
    RouteTableId=rtrep3['RouteTable']['RouteTableId'],
    SubnetId=l[1],
)


#**********************************************************************






#**********************EC2 insatnces**********************************

#instance1

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
            'SubnetId': l[0],    # Must be defined here
            'Groups': [rsg1['GroupId']],       # Security Group IDs go here
        }],

    UserData='''#!/bin/bash
dnf install -y git
git clone https://github.com/Skav0/Multi-tier-Web-Application-hosted-in-AWS.git
dnf install -y httpd
systemctl start httpd
systemctl enable httpd
mkdir /var/www/html/
mv /Multi-tier-Web-Application-hosted-in-AWS/index.html /var/www/html'''
)



#instance2 
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
            'SubnetId': l[1],    # Must be defined here
            'Groups': [rsg2['GroupId']],       # Security Group IDs go here
        }],

    UserData='''#!/bin/bash
dnf install -y git
git clone https://github.com/Skav0/Multi-tier-Web-Application-hosted-in-AWS.git
dnf install -y httpd
systemctl start httpd
systemctl enable httpd
mkdir /var/www/html/
mv /Multi-tier-Web-Application-hosted-in-AWS/index.html /var/www/html'''
)




##########################################################################################



#*************************ALB**************************************

client = boto3.client('elbv2')

#alb1


response = client.create_load_balancer(
    Name='testingloadbalancer1adam',
    Subnets=[
        l[0],l[1]
    ],
  
    SecurityGroups=[
        rsg1['GroupId'],
    ],
    Scheme='internet-facing',
    
    Type='application',
    
)

#alb2
response = client.create_load_balancer(
    Name='testingloadbalancer2adam',
    Subnets=[
        l[0],l[1]
    ],
  
    SecurityGroups=[
        rsg2['GroupId'],
    ],
    Scheme='internet-facing',
    
    Type='application',
    
)






#correct the alb nat pointing instead of igw.
#******make sure the alb are working fine in the future********
#create target group for alb1
ralb1 = client.create_target_group(
    Name='targetgroup1adam',
    Port=80,
    Protocol='HTTP',
    VpcId=rvpc['Vpc']['VpcId'],
    TargetType='instance',
)
#create target group for alb2
ralb1 = client.create_target_group(
    Name='targetgroup2adam',
    Port=80,
    Protocol='HTTP',
    VpcId=rvpc['Vpc']['VpcId'],
    TargetType='instance',
)
#in the future create the asg for the 2 instances
