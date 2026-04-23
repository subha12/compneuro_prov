import re
import json

def parse_jobinfo(file_path):
    metadata = {}

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if "=" in line:
            key, value = line.split("=", 1)
            metadata[key.strip()] = value.strip()

    # Normalize important fields
    parsed = {
        "job_id": metadata.get("JOBID"),
        "task_id": metadata.get("Task ID"),
        "tool": metadata.get("Tool"),
        "job_handle": metadata.get("JobHandle"),
        "resource": metadata.get("resource"),
        "user_id": metadata.get("User ID"),
        "username": metadata.get("User Name"),
        "email": metadata.get("email"),
        "created_on": metadata.get("created on"),
    }

    return parsed


if __name__ == "__main__":
    import sys
    result = parse_jobinfo(sys.argv[1])
    print(json.dumps(result, indent=2))
  
