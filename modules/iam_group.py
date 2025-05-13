# modules/iam_group.py

import boto3
import json
import botocore
from datetime import datetime

iam = boto3.client('iam')

def create_group_with_policy(group_name, service, actions):
    try:
        # Check if group exists
        iam.get_group(GroupName=group_name)
        print(f"✅ Group '{group_name}' already exists.")
    except iam.exceptions.NoSuchEntityException:
        # Create the group if it doesn't exist
        iam.create_group(GroupName=group_name)
        print(f"✅ Group '{group_name}' created.")

    # Step 2: Build the policy
    policy_name = f"{group_name}_{service}_Policy"
    policy_document = build_policy(service, actions)

    try:
        # Create Managed Policy
        response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document),
            Description=f"Auto-created policy for {group_name} - {service}"
        )
        policy_arn = response['Policy']['Arn']
        print(f"✅ Managed policy '{policy_name}' created.")
    except iam.exceptions.EntityAlreadyExistsException:
        # If already exists, get ARN
        policy_arn = f"arn:aws:iam::aws:policy/{policy_name}"
        print(f"⚠️ Policy '{policy_name}' already exists. Using existing ARN.")

    # Step 3: Attach the policy to the group
    try:
        iam.attach_group_policy(
            GroupName=group_name,
            PolicyArn=policy_arn
        )
        print(f"🔗 Policy attached to group '{group_name}' successfully.\n")
    except botocore.exceptions.ClientError as e:
        print(f"❌ Error attaching policy: {e.response['Error']['Message']}")


def build_policy(service, actions):
    # Normalize actions to AWS format
    formatted_actions = [f"{service.lower()}:{action.strip()}" for action in actions]

    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": formatted_actions,
                "Resource": "*"
            }
        ]
    }
