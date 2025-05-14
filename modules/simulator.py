# modules/simulator.py

import subprocess
import json
from modules.simulator_log import log_simulation, log_error

def simulate_policy_from_file_data(policy_file, action, resource, principal_arn):
    log_simulation(f"\n🔍 Simulating action `{action}` on `{resource}` for `{principal_arn}` using policy `{policy_file}`")

    try:
        # Read policy JSON
        with open(policy_file, 'r') as f:
            policy = json.load(f)

        policy_str = json.dumps(policy)

        # Call AWS CLI to simulate custom policy
        result = subprocess.run([
            "aws", "iam", "simulate-custom-policy",
            "--policy-input-list", policy_str,
            "--action-names", action,
            "--resource-arns", resource,
            "--cli-binary-format", "raw-in-base64-out"
        ], capture_output=True, text=True)

        # Log AWS CLI output
        log_simulation(f"AWS CLI Result: {result.stdout}")

        # Check if the result is empty or if there was an error
        if result.returncode != 0:
            log_error(f"❌ Error during simulation: {result.stderr}")
            return {"EvalDecision": "implicitDeny", "error_message": result.stderr}

        # Check if no output was returned
        if not result.stdout:
            log_error("❌ No output from the simulation command.")
            return {"EvalDecision": "implicitDeny", "error_message": "No output from simulation"}

        try:
            # Parse the result as JSON
            output = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            log_error(f"❌ JSON decode error: {str(e)}")
            log_error(f"Raw output: {result.stdout}")
            return {"EvalDecision": "implicitDeny", "error_message": "Invalid JSON response"}

        log_simulation("\n✅ Simulation Result:")
        log_simulation(json.dumps(output, indent=4))

        # Extract the IAM decision (allow or deny)
        if "EvaluationResults" in output and output["EvaluationResults"]:
            decision = output["EvaluationResults"][0].get("EvalDecision", "implicitDeny")
            log_simulation(f"🔎 IAM says: {decision}")
            return {"EvalDecision": decision}

        # If no results found, return implicitDeny
        log_error("❌ No evaluation results found.")
        return {"EvalDecision": "implicitDeny", "error_message": "No evaluation results found"}

    except Exception as e:
        log_error(f"⚠️ Exception: {str(e)}")
        return {"EvalDecision": "implicitDeny", "error_message": str(e)}
