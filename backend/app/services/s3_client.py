import boto3

# Use EC2 IAM role automatically (no env vars needed)
s3 = boto3.client("s3")
