
import boto3 

client = boto3.client('elbv2')




response = client.create_load_balancer(
    Name='testingloadbalancer1adam',
    Subnets=[
        'subnet-052e7914a251c9cdd',
    ],
  
    SecurityGroups=[
        'sg-080943c75e79699af',
    ],
    Scheme='internet-facing',
    
    Type='application',
    
)