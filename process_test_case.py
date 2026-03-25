import json
import sys
import subprocess
import os

def process_test_case(json_file_path):
    """Process a single test case JSON file through Phase 1 and Phase 2"""
    
    # Read the combined JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    metadata = data['metadata']
    test_steps = data['testSteps']
    
    # Create temp files
    metadata_file = 'temp_metadata.json'
    steps_file = 'temp_steps.json'
    
    # Save metadata to temp file
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Processing: {metadata['name']}")
    print(f"{'='*70}")
    
    # Phase 1: Create test case metadata
    print("\n🔹 Phase 1: Creating test case metadata...")
    result = subprocess.run(
        ['python', 'create_zephyr_test.py', metadata_file],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.returncode != 0:
        print(f"Phase 1 failed: {result.stderr}")
        return None
    
    # Extract test case key from output
    test_case_key = None
    for line in result.stdout.split('\n'):
        if 'Test Case Created:' in line:
            test_case_key = line.split(':')[-1].strip()
            break
    
    if not test_case_key:
        print("Could not extract test case key")
        return None
    
    print(f"Test Case Key: {test_case_key}")
    
    # Save steps to temp file
    with open(steps_file, 'w') as f:
        json.dump(test_steps, f, indent=2)
    
    # Phase 2: Attach test steps
    print(f"\n🔹 Phase 2: Attaching test steps to {test_case_key}...")
    result = subprocess.run(
        ['python', 'post_zephyr_steps.py', test_case_key, steps_file],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.returncode != 0:
        print(f"Phase 2 failed: {result.stderr}")
        return None
    
    # Cleanup temp files
    if os.path.exists(metadata_file):
        os.remove(metadata_file)
    if os.path.exists(steps_file):
        os.remove(steps_file)
    
    print(f"Completed: {test_case_key}")
    return test_case_key

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_test_case.py <json_file_path>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    process_test_case(json_file)
