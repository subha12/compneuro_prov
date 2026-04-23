import yaml
import sys
import os
import hashlib
from metadata_extraction.parse_jobinfo import parse_jobinfo


def compute_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def generate_clu_yaml(jobinfo_path, output_yaml, output_dir):
    data = parse_jobinfo(jobinfo_path)

    yaml_data = {
        "Token": "need_a_token_if_not_passed_as_a_cmdline_param",

        # REQUIRED
        "Directories": [output_dir],

        "ExcludeList": [],

        "Title": f"NSG Job {data['job_id']} - {data['tool']}",

        "Description": (
            f"Provenance record for NSG job execution.\n"
            f"Tool: {data['tool']}, Resource: {data['resource']}, "
            f"User: {data['username']}, Created: {data['created_on']}"
        ),

        "Keywords": f"NSG, HPC, {data['tool']}",

        "DOI": "",

        "URL": "http://nsgportal.org",

        "Funding": [
            {"NSF": True},
            {"NIH": False},
            {"NASA": False},
            {"NOAA": False}
        ],

        "Acknowledgment": (
            "Automatically generated provenance metadata from NSG workflow."
        )
    }

    with open(output_yaml, "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False)

    print(f"Generated CLU YAML: {output_yaml}")


if __name__ == "__main__":
    jobinfo = sys.argv[1]
    output_yaml = sys.argv[2]
    output_dir = sys.argv[3]

    generate_clu_yaml(jobinfo, output_yaml, output_dir)
  
