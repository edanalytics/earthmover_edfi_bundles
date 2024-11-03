import json
from pathlib import Path
import sys

from yaml import safe_load

root = sys.argv[1]
md = {}
all_bundles = []

root_path = Path(root)
for sub_dir in root_path.iterdir():
    metadata_file = Path(sub_dir / "_metadata.yaml")
    if metadata_file.exists():
        with open(metadata_file) as stream:
            md = safe_load(stream)
            all_bundles.append(md)

with open('registry.json', 'w') as fp:
    json.dump({"assessments": all_bundles}, fp)