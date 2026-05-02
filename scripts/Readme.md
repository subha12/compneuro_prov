When a job runs on Neuroscience Gateway, the gateway creates _JOBINFO.txt. 
The following workflow, as outlined below, uses the metadata from _JOBINFO.txt, parses and creates the OSC specific yaml, and submits to the OSC blockchain. THe confirmation ID from the blockchain is inserted into the OSC database. 

_JOBINFO.txt -> parse_jobinfo.py -> generate_clu_yaml.py -> output.yaml -> submit_to_osc.py -> Blockchain ID -> MySQL mapping

Steps to Run: 

This assumes that the CLU client (../Auxillary/osc_client.py) has been downloaded and available

python scripts/generate_clu_yaml.py path/to/_JOBINFO.txt output.yaml
python scripts/submit_to_osc.py output.yaml job_id user_id

What Happens Internally:
CLU call:
python auxiliary/CLU/osc_client.py contribute --template output.yaml --token <token>

Expected output (example):

Contribution successful
OSC ID: osc-abc123xyz

