# main.py

from modules import iam_user, iam_group, policy_builder, cross_account
import sys

def main():
    print("\n🚀 Welcome to IAM AutoBuilder Tool\n")
    
    while True:
        print("Choose an action:")
        print("1. Create IAM Group & Attach Policy")
        print("2. Create IAM Users and Assign to Groups")
        print("3. Create Cross-Account Role")
        print("4. Exit\n")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            group_name = input("🔹 Enter IAM Group Name: ").strip()
            service = input("🔹 AWS Service? (e.g., EC2, S3): ").strip()
            permissions = input("🔹 Permissions (comma-separated, e.g., StartInstances, DescribeInstances): ").strip().split(",")
            iam_group.create_group_with_policy(group_name, service, permissions)

        elif choice == "2":
            username = input("🔹 Enter IAM Username: ").strip()
            group = input("🔹 Assign to Group: ").strip()
            mfa = input("🔹 Require MFA? (yes/no): ").strip().lower() == 'yes'
            iam_user.create_user(username, group, mfa)

        elif choice == "3":
            role_name = input("🔹 Role Name: ").strip()
            external_account_id = input("🔹 External AWS Account ID: ").strip()
            duration = int(input("🔹 Session Duration (seconds): ").strip())
            cross_account.create_cross_account_role(role_name, external_account_id, duration)

        elif choice == "4":
            print("\n👋 Exiting. Thanks for using IAM AutoBuilder.")
            sys.exit(0)

        else:
            print("❗ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
