import boto3

s=input('give me the cidr block of the vpc: \n')
client = boto3.resource('ec2')

response = client.create_vpc(
    CidrBlock=s,
)
print(type(response))

exit()
n=int(input('give the number of subents that you wanna create: \n'))
print('choose the VPC Id that you wanna create the subnets on: \n')



'''
for i in range(n):
    s1=input('give the cidr block of the subnet that you wanna work on')
    response = client.create_subnet(
        CidrBlock='10.0.1.0/24',
        VpcId='vpc-a01106c2',
    )

'''