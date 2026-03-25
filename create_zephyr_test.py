import requests
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

def create_test_case(test_data):
    url = "https://api.zephyrscale.smartbear.com/v2/testcases"
    headers = {
        "Authorization": f"Bearer {os.getenv('ZEPHYR_TOKEN')}",
        "Content-Type": "application/json"
    }

    # Extract metadata from the JSON file
    metadata = test_data.get("metadata")
    if not metadata:
        print("Error: Metadata is missing in the JSON file.")
        return

    response = requests.post(url, headers=headers, json=metadata)

    if response.status_code == 201:
        print(f"Success! Test Case Created: {response.json().get('key')}")
    else:
        print(f"Failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Accept either JSON string or file path
    arg = sys.argv[1]
    if arg.endswith('.json'):
        with open(arg, 'r') as f:
            test_json = json.load(f)
    else:
        test_json = json.loads(arg)
    create_test_case(test_json)