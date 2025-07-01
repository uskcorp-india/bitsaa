import os
import json

def lambda_handler(event, context):
    print(json.dumps(event, indent=2))
    headers = event.get("headers") or {}
    print(f"headers : {headers}")
    signature = headers.get("X-Tikkl-Signature")
    if not signature:
        print("Missing X-Tikkl-Signature header")
        return deny()
    expected_secret = os.environ.get("TIKKL_SECRET")
    if not expected_secret:
        print("Missing TIKKL_SECRET env var")
        return deny()
    if signature == expected_secret:
        return allow(event["methodArn"])
    else:
        print("Signature mismatch")
        return deny()

def allow(resource):
    return generate_policy("authorized", "Allow", resource)

def deny():
    return generate_policy("unauthorized", "Deny", "*")

def generate_policy(principal_id, effect, resource):
    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Effect": effect,
                "Resource": resource
            }]
        }
    }

