import boto3
#**************************creating a vpc.*****************************************
client = boto3.resource('ec2')

response = client.create_vpc(
    CidrBlock='192.168.0.0/16',
)

x=str(response)
x=x[x.find('=')+2:-2]
print(x)



#**********************subnets************************************************



#After creating the vpc, i used the vpc id in the subnets below, and i included the zones where i can create the subnets.

response = client.create_subnet(
  
    AvailabilityZone='us-east-1a',
    CidrBlock='192.168.10.0/24',
    VpcId=x,
  
)


response = client.create_subnet(
  
    AvailabilityZone='us-east-1b',
    CidrBlock='192.168.20.0/24',
    VpcId=x,
  
)
response = client.create_subnet(
  
    AvailabilityZone='us-east-1c',
    CidrBlock='192.168.30.0/24',
    VpcId=x,
  
)


response = client.create_subnet(
  
    AvailabilityZone='us-east-1d',
    CidrBlock='192.168.40.0/24',
    VpcId=x,
  
)

#**********************************************************************