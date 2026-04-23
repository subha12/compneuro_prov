
## Overview
This repository provides a reference implementation for capturing,
serializing, and storing HPC job provenance metadata on blockchain infrastructure. This also has implementation of LSH for comparing parameters within model versions in computational neuroscience. The paper related to NSG-OSC integration - https://academic.oup.com/database/article/doi/10.1093/database/baae023/7641698


## Workflow
1. Job completes on NSG
2. Metadata extracted
3. JSON serialized
4. Submitted to OSC
5. Verified via reconciliation scripts
