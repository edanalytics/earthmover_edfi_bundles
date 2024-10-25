import json
from pprint import pprint
import sys

from yaml import safe_load

path = sys.argv[1]
md = {}

# TODO: update to find all instances
with open(path) as stream:
    md = safe_load(stream)

all_bundles = [md]


with open('registry.json', 'w') as fp:
    json.dump({"bundles": all_bundles}, fp)

"""
Okay, what's the plan

1. Start with an empty list of assesssments
2. If the file doesn't have any, then populate a single one with global_meta
3. Otherwise do a depth-first search down the tree, hanging onto the 'current' values of any fields and overwriting / appending as needed
    I really hope this doesn't encourage recursion but it might...

TODO: add repo name (arg), branch name (arg), and file path

"""

"""
Here's a place to put rules

input_params


"""