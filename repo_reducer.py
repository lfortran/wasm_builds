import os
import json
import shutil

DOCS_DIR = "docs"
DEV_DIR = os.path.join(DOCS_DIR, "dev")
RELEASE_DIR = os.path.join(DOCS_DIR, "release")


with open(os.path.join(DOCS_DIR, "data.json")) as fd:
    lf_versions = json.load(fd)

def delete_dir(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        print(f"Skipping deleting: {path}")


# remove everything in dev
for commit in lf_versions["dev"]:
    delete_dir(os.path.join(DEV_DIR, commit["lfortran_commit_sha"]))

# remove all except the commit used at dev.lfortran.org and newer
COMMIT_USED_AT_DEV_LFORTRAN_ORG = "7d0be2af5"
lf_release_commits = [lf["lfortran_commit_sha"] for lf in lf_versions["release"]]
commit_used_idx = lf_release_commits.index(COMMIT_USED_AT_DEV_LFORTRAN_ORG)

for commit in lf_versions["release"][commit_used_idx + 1:]:
    delete_dir(os.path.join(RELEASE_DIR, commit["lfortran_commit_sha"]))

# update data.json

lf_versions["dev"] = []
lf_versions["release"] = lf_versions["release"][:commit_used_idx + 1]

with open(os.path.join(DOCS_DIR, "data.json"), "w") as fd:
    json.dump(lf_versions, fd, indent=4)
