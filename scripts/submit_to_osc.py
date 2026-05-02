import os
import sys
import subprocess
import yaml
import re
import mysql.connector


def read_db_config(path="~/.db_config"):
    config = {}
    path = os.path.expanduser(path)

    with open(path, "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                config[k.strip()] = v.strip()

    return config


def run_clu_submit(template_yaml, token):
    cmd = [
        "python",
        "auxiliary/CLU/osc_client.py",
        "contribute",
        "--template",
        template_yaml,
        "--token",
        token
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("CLU submission failed")
        print(result.stderr)
        sys.exit(1)

    output = result.stdout
    print("CLU Output:\n", output)

    # Extract OSC ID (assumes output contains something like: OSC ID: XXXXX)
    match = re.search(r"(OSC[- ]?ID[: ]+)(\S+)", output, re.IGNORECASE)

    if not match:
        print("Could not extract OSC ID from CLU output")
        sys.exit(1)

    osc_id = match.group(2)
    return osc_id


def insert_into_db(job_id, user_id, osc_id):
    config = read_db_config()

    conn = mysql.connector.connect(
        host=config.get("host"),
        user=config.get("user"),
        password=config.get("password"),
        database=config.get("database")
    )

    cursor = conn.cursor()

    query = """
    INSERT INTO osc_job_info (job_id, user_id, osc_id)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE osc_id = %s
    """

    cursor.execute(query, (job_id, user_id, osc_id, osc_id))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted into DB: job_id={job_id}, osc_id={osc_id}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python submit_to_osc.py <output.yaml> <job_id> <user_id>")
    sys.exit(1)

    output_yaml = sys.argv[1]
    job_id = int(sys.argv[2])
    user_id = int(sys.argv[3])

    
    # Get token (from env or prompt)
    token = os.environ.get("OSC_TOKEN")
    if not token:
        token = input("Enter OSC token: ").strip()

    # Submit to CLU
    osc_id = run_clu_submit(output_yaml, token)

    #  Insert into DB
    insert_into_db(job_id, user_id, osc_id)


if __name__ == "__main__":
    main()
