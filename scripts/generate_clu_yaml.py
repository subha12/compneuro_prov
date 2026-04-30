import yaml
import sys
import os
from metadata_extraction.parse_jobinfo import parse_jobinfo


def read_full_jobinfo(jobinfo_path):
    with open(jobinfo_path, "r") as f:
        return f.read().strip()


def generate_clu_yaml(jobinfo_path, output_yaml):
    data = parse_jobinfo(jobinfo_path)

    # Full raw JOBINFO text
    description_text = read_full_jobinfo(jobinfo_path)

    # Funding mapping 
    funding_map = {
        "NSF": False,
        "NIH": False,
        "NASA": False,
        "NOAA": False
    }

    if "NSF" in description_text:
        funding_map["NSF"] = True
    if "NIH" in description_text:
        funding_map["NIH"] = True
    if "NASA" in description_text:
        funding_map["NASA"] = True
    if "NOAA" in description_text:
        funding_map["NOAA"] = True

    yaml_data = {
        "Token": "need_a_token_if_not_passed_as_a_cmdline_param",

        # Always current working directory
        "Directories": [os.getcwd()],

        "ExcludeList": [],

        "Title": data.get("tool", "NSG Job"),

        # Raw JOBINFO as description
        "Description": description_text,

        "Keywords": data.get("keywords", "NSG, HPC"),

        "DOI": "",

        "URL": "http://nsgportal.org",

        # Convert to required YAML format
        "Funding": [{k: v} for k, v in funding_map.items()],

        "Acknowledgment": "Automatically generated provenance metadata from NSG workflow."
    }

    with open(output_yaml, "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False)

    print(f"Generated CLU YAML: {output_yaml}")


if __name__ == "__main__":
    jobinfo = sys.argv[1]
    output_yaml = sys.argv[2]

    generate_clu_yaml(jobinfo, output_yaml)
