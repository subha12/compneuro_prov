When a job runs on Neuroscience Gateway, the gateway creates _JOBINFO.txt. 
The following workflow, as outlined below, uses the metadata from _JOBINFO.txt, parses and creates the OSC specific yaml, and submits to the OSC blockchain
_JOBINFO.txt -> parse_jobinfo.py -> generate_clu_yaml.py -> output.yaml -> clu submit

python scripts/generate_clu_yaml.py path/to/_JOBINFO.txt output.yaml
