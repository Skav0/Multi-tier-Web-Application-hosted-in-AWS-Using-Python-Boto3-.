import boto3


#create/deleting(if exist) the vpc.

y=int(input("Do you wanna create(1)/delete(2) a VPC?"))

if y==1:

    x=input('Enter your VPC CIDR block')
    client = boto3.resource('ec2')

    response=client.create_vpc(
        CidrBlock=x,

    )
    print(response)
elif y==2:
    #delete the vpc that you want


'''

#creating 6 subnets(2 public(for the load balancer) , 2 private(for the servers), 2 for the databases.)


client.create_subnet(
    
    CidrBlock='10.0.1.0/20',
    #redirect the VpcId 
    VpcId='vpc-a01106c2',
)
'''

