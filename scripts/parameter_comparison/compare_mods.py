import os
import hashlib
import argparse
import re
from collections import defaultdict

# ----------------------------
# Utility: SHA256
# ----------------------------
def compute_sha256_from_string(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_sha256_file(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# ----------------------------
# Step 1: Remove comments
# ----------------------------
def remove_comments(text: str) -> str:
    # Remove block comments
    text = re.sub(r"COMMENT.*?ENDCOMMENT", "", text, flags=re.DOTALL)

    # Remove single-line comments starting with :
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(":"):
            continue
        lines.append(line)

    return "\n".join(lines)


# ----------------------------
# Step 2: Extract and sort blocks
# ----------------------------
BLOCK_KEYWORDS = [
    "NEURON",
    "PARAMETER",
    "ASSIGNED",
    "STATE",
    "BREAKPOINT",
    "INITIAL",
    "DERIVATIVE",
    "PROCEDURE",
    "FUNCTION",
]


def extract_blocks(text: str):
    blocks = defaultdict(list)
    current_block = None
    buffer = []

    for line in text.splitlines():
        stripped = line.strip()

        # Detect block start
        if any(stripped.startswith(k) for k in BLOCK_KEYWORDS):
            if current_block:
                blocks[current_block].append("\n".join(buffer))
                buffer = []
            current_block = stripped.split()[0]
            buffer.append(line)
        else:
            buffer.append(line)

    if current_block and buffer:
        blocks[current_block].append("\n".join(buffer))

    return blocks


def normalize_content(text: str) -> str:
    text = remove_comments(text)
    blocks = extract_blocks(text)

    normalized_parts = []

    for block_name in sorted(blocks.keys()):
        for block_content in blocks[block_name]:
            # Normalize whitespace
            cleaned = "\n".join(line.strip() for line in block_content.splitlines() if line.strip())
            normalized_parts.append(cleaned)

    return "\n\n".join(normalized_parts)


# ----------------------------
# Load .mod files
# ----------------------------
def load_mod_files(directory):
    mod_files = {}
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".mod"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    mod_files[f] = file.read()
    return mod_files


# ----------------------------
# Main comparison logic
# ----------------------------
def compare_directories(dir1, dir2):
    files1 = load_mod_files(dir1)
    files2 = load_mod_files(dir2)

    results = {
        "exact_match": [],
        "functional_match": [],
        "different": [],
        "only_in_dir1": [],
        "only_in_dir2": []
    }

    all_files = set(files1.keys()).union(set(files2.keys()))

    for fname in all_files:
        if fname not in files1:
            results["only_in_dir2"].append(fname)
            continue
        if fname not in files2:
            results["only_in_dir1"].append(fname)
            continue

        raw_hash1 = compute_sha256_from_string(files1[fname])
        raw_hash2 = compute_sha256_from_string(files2[fname])

        if raw_hash1 == raw_hash2:
            results["exact_match"].append(fname)
            continue

        norm1 = normalize_content(files1[fname])
        norm2 = normalize_content(files2[fname])

        norm_hash1 = compute_sha256_from_string(norm1)
        norm_hash2 = compute_sha256_from_string(norm2)

        if norm_hash1 == norm_hash2:
            results["functional_match"].append(fname)
        else:
            results["different"].append(fname)

    return results


# ----------------------------
# CLI
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Compare NEURON .mod files across two directories")
    parser.add_argument("dir1", help="First directory containing mod_files")
    parser.add_argument("dir2", help="Second directory containing mod_files")

    args = parser.parse_args()

    results = compare_directories(args.dir1, args.dir2)

    print("\n=== Comparison Results ===\n")

    print("Exact Matches:")
    for f in results["exact_match"]:
        print(f"  - {f}")

    print("\nFunctional Matches (after normalization):")
    for f in results["functional_match"]:
        print(f"  - {f}")

    print("\nDifferent Files:")
    for f in results["different"]:
        print(f"  - {f}")

    print("\nOnly in Directory 1:")
    for f in results["only_in_dir1"]:
        print(f"  - {f}")

    print("\nOnly in Directory 2:")
    for f in results["only_in_dir2"]:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
