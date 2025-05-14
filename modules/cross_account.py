# modules/cross_account.py

import boto3
import json
from botocore.exceptions import ClientError

iam = boto3.client('iam')

def create_cross_account_role(role_name, trusted_account_id, dynamodb_actions=None):
    if dynamodb_actions is None:
        dynamodb_actions = ["dynamodb:GetItem", "dynamodb:PutItem"]

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{trusted_account_id}:root"
                },
                "Action": "sts:AssumeRole",
                "Condition": {}
            }
        ]
    }

    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": dynamodb_actions,
                "Resource": "*"
            }
        ]
    }

    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Cross-account role for contractor access to DynamoDB'
        )
        print(f"✅ Role '{role_name}' created for Account ID {trusted_account_id}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"⚠️ Role '{role_name}' already exists.")
        else:
            print(f"❌ Error: {e}")
            return

    # Attach inline policy to the role
    try:
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName=f"{role_name}Policy",
            PolicyDocument=json.dumps(policy_doc)
        )
        print(f"🔐 Inline policy attached to role '{role_name}' with DynamoDB actions.")
    except ClientError as e:
        print(f"❌ Failed to attach policy: {e}")

    print(f"🔗 Role ARN: arn:aws:iam::YOUR_ACCOUNT_ID:role/{role_name}")
