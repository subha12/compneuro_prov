## Parameter Comparison for NEURON MOD Files

This module provides a workflow to compare NEURON `.mod` files across two directories to determine whether they are identical 

NEURON models include multiple `.mod` files stored in a directory (https://neuronline.github.io/compneuro/software/neuron/nmodl/).

To compare if exact mod files are used between two models, this workflow compares the mod files for exact match and further compares the files after removal of comments and reordering of the blocks alphabetically. 

## Step 1: Raw File Comparison (Exact Match)

1. Traverse all `.mod` files in each directory
2. Compute SHA256 checksum for each file
3. Compare checksums across directories

### Output

* Exact matches (identical files)
* Non-matching files

---

## Step 2: Normalized Comparison

* Remove Comments: The following comment formats are removed:

 - Single-line comments
   E.g, Lines starting with:

```
: this is a comment
```

- Block comments

```
COMMENT
    This is a
    multi-line comment
ENDCOMMENT
```

---


After removing comments:

* Identify logical blocks (e.g., `NEURON`, `PARAMETER`, `ASSIGNED`, `BREAKPOINT`, etc.)
* Reorder blocks alphabetically
* Strip extra whitespace

Compute Normalized Hash

* Compute SHA256 checksum on the normalized content
* Compare across directories

---

## Output Categories

After both steps, files fall into:

1. **Exact Match**

   * Raw SHA256 identical

2. **Functional Match**

   * Raw differs, but normalized SHA256 identical

3. **Different**

   * No match even after normalization

---

## Example Workflow

```
Directory A: mod_files/
Directory B: mod_files/

Step 1 → Compare raw SHA256
Step 2 → Normalize → Compare again
```

---

NOTES: 

* This workflow assumes valid NEURON `.mod` file structure
* Block detection is based on standard NEURON syntax
* Additional normalization rules can be added if needed

---

## Future Improvements
* Similarity analysis using LSH
* Integration with provenance tracking pipeline

---

Example using https://modeldb.science/136803 where ca.mod was changed

% /usr/local/opt/python@3.9/bin/python3 compare_mods.py ../NSGrest/JonesEtAl2009/mod_files ../../Downloads/output-4/JonesEtAl2009/mod_files

=== Comparison Results ===

Exact Matches:
  - km.mod
  - ar.mod
  - cad.mod
  - pp_dipole.mod
  - dipole.mod
  - cat.mod
  - kca.mod

Functional Matches (after normalization):

Different Files:
  - ca.mod

Only in Directory 1:

Only in Directory 2:


An example `.mod` file is included in this directory for testing and validation.
