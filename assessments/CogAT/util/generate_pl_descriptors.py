# Generates a CSV with all the possible CogAT performance levels. These primarily
#   consist of "ability profiles," of which there are many.
#
#   Info on ability profiles: https://riversideinsights.com/citc/profile-finder
#
## HOW TO USE
# python generate_pl_descriptors.py [outfile.csv]
# Example:
# python preprocessing.py seeds/performanceLevelDescriptors.csv

import sys
import pandas as pd

outfile = sys.argv[1]


mods = ["V-", "V+", "Q-", "Q+", "N-", "N+"]

# initialize with non-abilityProfile values
pls = [
    {"codeValue": "Y", "description": "Yes", "shortDescription": "Y"},
    {"codeValue": "N", "description": "No", "shortDescription": "N"},
    {"codeValue": "N/A", "description": "Not applicable", "shortDescription": "N/A"},
]

# stanines 1-9
for stanine in range(1, 10):
    # A is just stanine and profile
    profile = f"{stanine}A"
    pls.append({"codeValue": profile, "description": "", "shortDescription": profile})
    # B is stanine, profile, and one modifier
    for mod in mods:
        profile = f"{stanine}B ({mod})"
        pls.append(
            {"codeValue": profile, "description": "", "shortDescription": profile}
        )
    # C is stanine, profile, and two modifiers
    for mod in mods:
        for mod_x in mods:
            if mod[0] != mod_x[0] and mod[1] != mod_x[1]:
                # modifiers must be from different tests and directions
                profile = f"{stanine}C ({mod}{mod_x})"
                pls.append(
                    {
                        "codeValue": profile,
                        "description": "",
                        "shortDescription": profile,
                    }
                )
    # E is stanine, profile, and one or two modifiers
    for mod in mods:
        profile = f"{stanine}E ({mod})"
        pls.append(
            {"codeValue": profile, "description": "", "shortDescription": profile}
        )
    for mod in mods:
        for mod_x in mods:
            if mod[0] != mod_x[0] and mod[1] != mod_x[1]:
                # modifiers must be from different tests and directions
                profile = f"{stanine}E ({mod}{mod_x})"
                pls.append(
                    {
                        "codeValue": profile,
                        "description": "",
                        "shortDescription": profile,
                    }
                )

pl_df = pd.DataFrame(pls)
pl_df["namespace"] = (
    "uri://www.riversideinsights.com/cognitive_abilities_test/PerformanceLevelDescriptor"
)

pl_df.to_csv(outfile, index=False)
