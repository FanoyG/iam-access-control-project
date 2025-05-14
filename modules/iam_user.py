# modules/iam_user.py

import boto3
import botocore

iam = boto3.client('iam')

def create_user(username, group_name, require_mfa=False):
    try:
        # Create IAM User
        iam.get_user(UserName=username)
        print(f"✅ User '{username}' already exists.")
    except iam.exceptions.NoSuchEntityException:
        iam.create_user(UserName=username)
        print(f"✅ User '{username}' created.")

    # Add user to group
    try:
        iam.add_user_to_group(UserName=username, GroupName=group_name)
        print(f"🔗 User '{username}' added to group '{group_name}'.")
    except botocore.exceptions.ClientError as e:
        print(f"❌ Error adding user to group: {e.response['Error']['Message']}")

    # Create login profile (console password access)
    try:
        iam.create_login_profile(
            UserName=username,
            Password="TempPass#123",  # In real-world, generate/send securely
            PasswordResetRequired=True
        )
        print(f"🧾 Console login enabled for '{username}' (TempPass#123).")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"⚠️ Console login already enabled for '{username}'.")

    # Placeholder for MFA setup
    if require_mfa:
        print(f"🔐 MFA setup should be done manually via Console or CLI for '{username}'.")
