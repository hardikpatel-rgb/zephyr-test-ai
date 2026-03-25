import requests
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

def post_test_steps(test_case_key, steps_data):
    url = f"https://api.zephyrscale.smartbear.com/v2/testcases/{test_case_key}/teststeps"

    headers = {
        "Authorization": f"Bearer {os.getenv('ZEPHYR_TOKEN')}",
        "Content-Type": "application/json"
    }

    # Validate payload
    if "items" not in steps_data or not steps_data["items"]:
        print("Invalid payload: 'items' array missing or empty.")
        sys.exit(1)

    payload = {
        "mode": "OVERWRITE",
        "items": steps_data["items"]
    }

    print("Sending payload:")
    print(json.dumps(payload, indent=2))

    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        print(f"Steps successfully added to {test_case_key}")
        print("Response:", response.json())
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post_zephyr_steps.py <TEST_CASE_KEY> '<JSON_SCRIPT_DATA>'")
        sys.exit(1)
        
    case_key = sys.argv[1]
    arg = sys.argv[2]
    
    # Accept either JSON string or file path
    if arg.endswith('.json'):
        with open(arg, 'r') as f:
            script_json = json.load(f)
    else:
        # Join in case the shell split the JSON string
        raw_json = " ".join(sys.argv[2:])
        script_json = json.loads(raw_json)
    
    # Extract testSteps from the JSON file
    steps_data = script_json.get("testSteps")
    if not steps_data:
        print("Error: 'testSteps' section is missing in the JSON file.")
        sys.exit(1)

    post_test_steps(case_key, steps_data)