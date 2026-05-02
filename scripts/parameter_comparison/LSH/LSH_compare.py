import json
import argparse
from pprint import pprint
from typing import Dict, Any, List
from pathlib import Path
from deepdiff import DeepDiff

from lib import apply_lsh


TARGET_PARAMS = ["connParams"]


def load_netpyne_params(file_path: Path) -> Dict[str, Any]:
    """Load NetPyne JSON and extract parameter section."""
    with file_path.open("r") as f:
        data = json.load(f)

    if "net" not in data or "params" not in data["net"]:
        raise ValueError(f"{file_path} missing required 'net.params' structure")

    return data["net"]["params"]


def extract_target_params(params: Dict[str, Any]) -> Dict[str, str]:
    """Convert selected parameter blocks into canonical JSON strings."""
    extracted = {}

    for key in TARGET_PARAMS:
        if key not in params:
            raise KeyError(f"Missing key: {key}")

        value = params[key] if params[key] else {}
        extracted[key] = json.dumps(value, sort_keys=True)

    return extracted


def collect_files(input_dir: str) -> List[Path]:
    """Return list of files in directory."""
    return [
        Path(input_dir) / f
        for f in Path(input_dir).iterdir()
        if f.is_file()
    ]


def run_analysis(args: argparse.Namespace) -> None:
    files = collect_files(args.input)

    parsed = {
        f: extract_target_params(load_netpyne_params(f))
        for f in files
    }

    results = {}

    for param in TARGET_PARAMS:
        dataset = [(f, parsed[f][param]) for f in files]

        result, pairs = apply_lsh(dataset, args.threshold)
        results[param] = (result, pairs)

    for param, (res, pairs) in results.items():
        print(f"\n=== Results for {param} ===")

        for f1, f2, score in pairs:
            print(f"{f1} vs {f2}: similarity = {score}")

            if abs(float(score) - 1.0) > 1e-4:
                obj1 = json.loads(parsed[f1][param])
                obj2 = json.loads(parsed[f2][param])

                if args.data:
                    print("\nFile 1:")
                    pprint(obj1)
                    print("\nFile 2:")
                    pprint(obj2)

                if args.diff:
                    print("\nDiff:")
                    pprint(DeepDiff(obj1, obj2, ignore_order=True))


def main():
    parser = argparse.ArgumentParser(description="NetPyne similarity checker")

    parser.add_argument("input")
    parser.add_argument("threshold", type=float)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--data", action="store_true")

    args = parser.parse_args()
    run_analysis(args)


if __name__ == "__main__":
    main()
