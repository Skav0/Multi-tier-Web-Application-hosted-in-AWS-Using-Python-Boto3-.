import boto3 

''''''
client = boto3.client('ec2')

rvpc = client.create_vpc(
    CidrBlock='192.168.0.0/16',
)



rsg1 = client.create_security_group(
    Description='Public SG',
    GroupName='Public SG',
    VpcId=rvpc['Vpc']['VpcId'],
)

print(rsg1['GroupId'])