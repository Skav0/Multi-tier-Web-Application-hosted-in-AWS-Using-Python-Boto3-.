# Multi-tier-Web-Application-hosted-in-AWS-Using-Python-Boto3-.
Creating a highly, auto scaled web app on aws cloud using python and boto3 library.

We will follow an architecture that we used in a previous repo to create a the same up but using the aws console. And right now, we will do the same thing but using boto3.
To see the architecture, look at "Architecture.png" image. We are not going to stick to the provided on the image, instead i will use my own naming label.
To know what i did exactly, you can read the comments on "Code.py" file.
I'll make this script flexible, so you can input your own configuration(like cidr, and names so it's more efficient)
I made the script flexible, so you can add your own number. And also you can delete the things that you created.
in the next section i will include what i did exactly so you can understand the flow:

###
-Created a vpc, and subnets on this vpc.
Got the vpc id from the response, and filtered the vpc id so i can take it as an input for the subnet creation script.

###