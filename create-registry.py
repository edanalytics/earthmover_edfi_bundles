import argparse
import json
from pathlib import Path

from yaml import safe_load

parser = argparse.ArgumentParser()
parser.add_argument("root")
parser.add_argument("--output", default="registry.json")
args = parser.parse_args()

all_bundles = []

root_path = Path(args.root)
for sub_dir in root_path.iterdir():
    metadata_file = Path(sub_dir / "_metadata.yaml")
    if metadata_file.exists():
        with open(metadata_file) as stream:
            md = safe_load(stream)
            all_bundles.append(md)

with open(args.output, "w") as fp:
    json.dump({"assessments": all_bundles}, fp)
