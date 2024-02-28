import sys
import boto3
import json

def add_statement_to_bucket_policy(bucket_name, new_statement):
    """
    Add a statement to the S3 bucket policy.
    """
    client_s3 = boto3.client(
        's3'
    )
    
    # Get the current bucket policy
    current_policy = client_s3.get_bucket_policy(Bucket=bucket_name)
    current_policy_statement = current_policy['Policy']
    current_policy_statement_json = json.loads(current_policy_statement)
    
    # Add the new statement to the existing statements
    current_policy_statement_json['Statement'].append(new_statement)
    
    # Convert the modified policy back to JSON string
    updated_policy = json.dumps(current_policy_statement_json)
    print(updated_policy)
    
    # Update the bucket policy
    client_s3.put_bucket_policy(Bucket=bucket_name, Policy=updated_policy)
    print("Statement added to bucket policy successfully.")

# Function to process each CSV line
def process_csv_line(account_id, distribution_id, bucket):
    # Your existing logic here...
    # Use account_id, distribution_id, and bucket in your logic
    new_statement = {
        "Sid": "AllowCloudFrontOACReadWrite",
        "Effect": "Allow",
        "Principal": {"Service": "cloudfront.amazonaws.com"},
        "Action": [
            "s3:GetObject",
            "s3:PutObject"
        ],
        "Resource": "arn:aws:s3:::%s/*" % bucket,
        "Condition": {
            "StringEquals": {
                "AWS:SourceArn": "arn:aws:cloudfront::%s:distribution/%s" % (account_id, distribution_id)
            }
        }
    }
    add_statement_to_bucket_policy(bucket, new_statement)

# Read the CSV file and iterate through lines
with open('map.csv', 'r') as file:
    for line in file:
        # Assuming your CSV format is: cloudfront_account_id, cloudfront_distribution_id, bucket_name
        parts = line.strip().split(',')
        if len(parts) == 3:
            cloudfront_account_id, cloudfront_distribution_id, bucket_name = parts
            process_csv_line(cloudfront_account_id, cloudfront_distribution_id, bucket_name)
        else:
            print("Invalid CSV format")
