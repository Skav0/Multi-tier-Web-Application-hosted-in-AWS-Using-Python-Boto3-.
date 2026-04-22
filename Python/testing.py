
import boto3 

client=boto3.client('ec2')
#*****creating EIPs for the NAT GWs***

reip1 = client.allocate_address(
    Domain='vpc',
)
reip2 = client.allocate_address(
    Domain='vpc',
)
#******************************

