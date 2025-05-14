import boto3

def remove_user_resources(iam, user_name):
    # Remove from all groups
    groups = iam.list_groups_for_user(UserName=user_name)['Groups']
    for group in groups:
        print(f"Removing {user_name} from group {group['GroupName']}")
        iam.remove_user_from_group(UserName=user_name, GroupName=group['GroupName'])

    # Detach managed policies
    policies = iam.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
    for policy in policies:
        print(f"Detaching policy {policy['PolicyArn']} from user {user_name}")
        iam.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])

    # Delete inline policies
    inline_policies = iam.list_user_policies(UserName=user_name)['PolicyNames']
    for policy_name in inline_policies:
        print(f"Deleting inline policy {policy_name} from user {user_name}")
        iam.delete_user_policy(UserName=user_name, PolicyName=policy_name)

    # Delete access keys
    access_keys = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
    for key in access_keys:
        print(f"Deleting access key {key['AccessKeyId']} for user {user_name}")
        iam.delete_access_key(UserName=user_name, AccessKeyId=key['AccessKeyId'])

    # Delete signing certificates
    certs = iam.list_signing_certificates(UserName=user_name)['Certificates']
    for cert in certs:
        print(f"Deleting signing certificate {cert['CertificateId']} for user {user_name}")
        iam.delete_signing_certificate(UserName=user_name, CertificateId=cert['CertificateId'])

    # Delete SSH public keys
    ssh_keys = iam.list_ssh_public_keys(UserName=user_name)['SSHPublicKeys']
    for ssh_key in ssh_keys:
        print(f"Deleting SSH public key {ssh_key['SSHPublicKeyId']} for user {user_name}")
        iam.delete_ssh_public_key(UserName=user_name, SSHPublicKeyId=ssh_key['SSHPublicKeyId'])

    # Delete service-specific credentials
    creds = iam.list_service_specific_credentials(UserName=user_name)
    for cred in creds.get('ServiceSpecificCredentials', []):
        print(f"Deleting service-specific credential {cred['ServiceSpecificCredentialId']} for user {user_name}")
        iam.delete_service_specific_credential(UserName=user_name, ServiceSpecificCredentialId=cred['ServiceSpecificCredentialId'])

    # Deactivate and delete MFA devices
    mfa_devices = iam.list_mfa_devices(UserName=user_name)['MFADevices']
    for mfa in mfa_devices:
        print(f"Deactivating and deleting MFA device {mfa['SerialNumber']} for user {user_name}")
        try:
            iam.deactivate_mfa_device(UserName=user_name, SerialNumber=mfa['SerialNumber'])
        except Exception:
            pass  # Ignore if already deactivated
        try:
            iam.delete_virtual_mfa_device(SerialNumber=mfa['SerialNumber'])
        except Exception:
            pass  # Ignore if not a virtual device

def delete_user(iam, user_name):
    print(f"\nProcessing user: {user_name}")
    remove_user_resources(iam, user_name)
    print(f"Deleting user {user_name}")
    iam.delete_user(UserName=user_name)

def main():
    iam = boto3.client('iam')
    user_name = input("Enter the IAM username to delete: ")
    delete_user(iam, user_name)

if __name__ == "__main__":
    main()
