# modules/policy_builder.py

import subprocess
import os
import datetime
import json
from modules.simulator import simulate_policy_from_file_data

def create_custom_policy(service=None, actions=None, resources=None):
    print("\n🛠️  IAM Policy Builder")

    policy = {
        "Version": "2012-10-17",
        "Statement": []
    }

    # 🧠 If service, actions, and resources are provided — skip interactive part
    if service and actions and resources:
        statement = {
            "Effect": "Allow",  # Default effect when auto-building
            "Action": [f"{service.lower()}:{a.strip()}" for a in actions],
            "Resource": resources
        }
        policy["Statement"].append(statement)
        return policy

    # 🔁 Fallback to interactive policy creation
    while True:
        effect = input("➕ Enter Effect (Allow/Deny): ").strip().title()
        if effect not in ["Allow", "Deny"]:
            print("❌ Invalid effect. Try again.")
            continue

        actions = input("🔹 Enter AWS Actions (comma-separated, e.g., ec2:StartInstances,ec2:DescribeInstances): ").strip()
        actions_list = [a.strip() for a in actions.split(",") if a.strip()]
        if not actions_list:
            print("❌ No actions provided.")
            continue

        resource = input("📍 Enter Resource ARN (or * for all resources): ").strip()

        statement = {
            "Effect": effect,
            "Action": actions_list,
            "Resource": resource
        }

        policy["Statement"].append(statement)

        another = input("➕ Add another statement? (yes/no): ").strip().lower()
        if another != 'yes':
            break

    print("\n✅ Generated Policy:")
    print(json.dumps(policy, indent=4))

    # 🔍 Simulation Phase
    simulate = input("\n🔎 Do you want to validate this policy now? (yes/no): ").strip().lower()
    if simulate == "yes":
        principal_arn = input("👤 Enter IAM Principal ARN (user/role): ").strip()
        action = input("🔹 Enter action to simulate (e.g., s3:ListBucket): ").strip()
        sim_resource = input("📍 Enter resource ARN to test on: ").strip()

        simulate_policy_from_file_data(policy, action, sim_resource, principal_arn)

    # 💾 Ask to Save
    save = input("\n💾 Save this policy to file? (yes/no): ").strip().lower()
    if save == "yes":
        filename = input("📄 Enter filename to save (e.g., my_policy.json): ").strip()
        save_policy_to_file(policy, filename)
    else:
        print("🚫 Policy not saved.")

    return policy


def save_policy_to_file(policy, filename="custom_policy.json"):
    # Create the folder if it doesn't exist
    folder_path = "result_saved_json"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Save the policy to the specified file inside the folder
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w") as f:
        json.dump(policy, f, indent=4)
    print(f"📁 Policy saved to {file_path}")


# Inline simulation helper (reuses logic from simulator.py)

def simulate_policy_from_file_data(policy_dict, action, resource, principal_arn):

    try:
        policy_str = json.dumps(policy_dict)

        result = subprocess.run([
            "aws", "iam", "simulate-custom-policy",
            "--policy-input-list", policy_str,
            "--action-names", action,
            "--resource-arns", resource,
            "--cli-binary-format", "raw-in-base64-out"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ Error during simulation:", result.stderr)
            return

        output = json.loads(result.stdout)
        decision = output["EvaluationResults"][0]["EvalDecision"]

        print("\n✅ Simulation Result:")
        print(json.dumps(output, indent=4))
        print(f"🔎 IAM Decision: {decision}")

        # ✅ Logging
        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "principal_arn": principal_arn,
            "action": action,
            "resource": resource,
            "decision": decision
        }

        os.makedirs("logs", exist_ok=True)
        log_file = "logs/simulation_log.json"

        # Append to log file
        if os.path.exists(log_file):
            with open(log_file, "r+") as f:
                logs = json.load(f)
                logs.append(log_entry)
                f.seek(0)
                json.dump(logs, f, indent=4)
        else:
            with open(log_file, "w") as f:
                json.dump([log_entry], f, indent=4)

        print(f"📝 Log saved to {log_file}")

    except Exception as e:
        print(f"⚠️ Error in inline simulation: {str(e)}")
