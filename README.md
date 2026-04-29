## Overview
This implementation is a prototype developed and tested on NSG and OSC. While the overall workflow is generalizable, users attempting to replicate this system on other computational platforms or blockchain frameworks should expect differences in APIs, job schedulers, and metadata availability.

Related publicaton - https://academic.oup.com/database/article/doi/10.1093/database/baae023/7641698?login=false

The scripts folder includes an implementation of Locality-Sensitive Hashing (LSH) for comparing parameter configurations across model versions in computational neuroscience workflows.

## Workflow
The NSG–OSC integration follows this workflow:
- Job execution completes on NSG
- Metadata is extracted from job outputs
- Metadata is serialized into JSON format
- JSON is submitted to OSC via API
- Transactions are verified using reconciliation scripts

## Troubleshooting and Replication Considerations

# Tested Environment: 
The prototype was validated in the following environment:
Neuroscience Gateway (NSG): CIPRES version R43 (SciGaP-CIPRES)
Open Science Chain (OSC): Hyperledger Fabric v2.3
Application: Neuro-Integrative Connectivity (NIC) v0.0.1
Database: MySQL v8.0 (NSG backend)
Programming Languages: Python 3, Bash
HPC Resource: Expanse Supercomputer (SLURM scheduler)
Hashing: SHA-256 via Python hashlib
LSH Library: pylsh (MinHash-based similarity)

Differences in versions or system configurations may require modification of scripts and APIs.

# Adapting to Other Computational Platforms:

The current implementation assumes an NSG-based HPC workflow. When adapting to other environments (e.g., SLURM clusters, cloud platforms):

- Metadata Extraction: 
* NSG-specific outputs (e.g., _JOBINFO.txt) may not exist
* Equivalent metadata must be obtained from the application and scheduler logs (e.g., SLURM, PBS)
- Execution Environment Capture
* Ensure consistent capture of:
  job ID, runtime, and resource allocation
  input/output file paths
  software versions

- Script Adaptation
* Parsing scripts must be updated to reflect platform-specific output formats

## Adapting to Other Blockchain Frameworks

This implementation uses OSC (Hyperledger Fabric). When using other blockchain systems:

- API Integration
* Replace OSC-specific API calls with the target system’s API
* Ensure support for submission, confirmation, and querying of transactions
- Data Model Adjustments
* Modify JSON schema as needed
* Account for transaction size or encoding constraints
- Verification Workflow
* Update reconciliation scripts based on how the new system exposes stored data

## Common Issues and Resolutions
1. Metadata Not Captured Correctly
Issue: Missing or incomplete metadata in JSON output
Cause: Inconsistent parsing of job output files
Resolution:
- Verify parsing logic
- Ensure consistent generation of _JOBINFO.txt (or equivalent)
- Validate required fields before serialization
2. Blockchain Submission Failures
Issue: Metadata is not recorded on the blockchain
Cause: API misconfiguration, authentication errors, or connectivity issues
Resolution:
- Confirm API endpoint and credentials
- Check network connectivity
- Update API calls if using a different blockchain framework
3. Hash Mismatch During Verification
Issue: Stored hashes do not match recomputed values
Cause: File modification or inconsistent file paths
Resolution:
- Perform hashing immediately after job completion
- Use consistent and absolute file paths
4. Inconsistent Job Status (e.g, NSG vs Blockchain)
Issue: Database and blockchain records do not align
Cause: Partial failures in metadata transmission
Resolution:
- Cross-check MySQL records with blockchain entries
- Re-run verification scripts
- Add logging checkpoints

## General Design Considerations
- Clearly define application-level metadata (e.g., model parameters) and infrastructure-level metadata (e.g., compute resources)
- Use a structured intermediate file (e.g., _JOBINFO.txt) for consistent metadata extraction
- Ensure consistent hashing methodology (e.g., SHA-256)
- While NIC was used for validation, the workflow can be extended to other tools (e.g., NEURON, )GENESIS) with appropriate parameter access
