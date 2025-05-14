from modules import iam_user, iam_group, policy_builder, cross_account, simulator
import sys
import time

def divider():
    print("\n" + "="*50 + "\n")

def main():
    divider()
    print("🚀 Welcome to IAM AutoBuilder Tool")
    print("🔐 Built for Real-World IAM Simulation\n")
    
    while True:
        print("Choose an action:")
        print("1️⃣  Create IAM Group & Attach Policy")
        print("2️⃣  Create IAM Users and Assign to Groups")
        print("3️⃣  Create Cross-Account Role")
        print("4️⃣  Advanced: Create & Simulate Custom Policy")
        print("5️⃣  Exit\n")

        choice = input("👉 Enter choice (1-5): ").strip()

        if choice == "1":
            # Create IAM Group & Attach Policy
            group_name = input("🔹 Enter IAM Group Name: ").strip()
            service = input("🔹 AWS Service? (e.g., EC2, S3, CloudWatch): ").strip()
            permissions = input("🔹 Permissions (comma-separated, e.g., StartInstances, DescribeInstances): ").strip()
            permissions_list = [perm.strip() for perm in permissions.split(",")]
            iam_group.create_group_with_policy(group_name, service, permissions_list)
            print("\n✅ IAM Group & Policy created successfully!")
        
        elif choice == "2":
            # Create IAM Users and Assign to Groups
            username = input("🔹 Enter IAM Username: ").strip()
            group = input("🔹 Assign to Group: ").strip()
            mfa = input("🔹 Require MFA? (yes/no): ").strip().lower() == 'yes'
            iam_user.create_user(username, group, mfa)
            print("\n✅ IAM User created and assigned to group successfully!")

        elif choice == "3":
            # Create Cross-Account Role
            role_name = input("🔹 Role Name: ").strip()
            external_account_id = input("🔹 External AWS Account ID: ").strip()
            duration_input = input("🔹 Session Duration (in seconds, default 3600): ").strip()
            try:
                duration = int(duration_input) if duration_input else 3600
            except ValueError:
                print("❌ Invalid duration. Using default 3600 seconds.")
                duration = 3600
            cross_account.create_cross_account_role(role_name, external_account_id, duration)
            print("\n✅ Cross-Account Role created successfully!")

        elif choice == "4":
            # Create policy using policy_builder
            policy = policy_builder.create_custom_policy()
            


if __name__ == "__main__":
    main()
