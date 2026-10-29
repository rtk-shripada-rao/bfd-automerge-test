# Testing the Auto-merge Workflow

## Prerequisites

- The `srsd-sigma-automation-pipeline` GitHub App is installed on this repo; test PRs must be opened by it.
- Repo secret `AUTOMERGE_PAT`: a PAT for a service account (not the app) with **Contents** and **Pull requests** read/write on this repo.

## Scenarios

| # | PR | Expected |
|---|---|---|
| 1 | Opened by the app, only changes `detections/engine/rule_status.json` | CI passes, PR is approved and merged |
| 2 | Opened by the app, also adds `unauthorized_file.txt` | "Check files changed" fails and lists the file; no merge |
| 3 | Opened by the app as a draft | Skips with "PR is draft"; marking it ready for review runs it again and merges |
| 4 | Opened by the app, breaks `rule_status.json` (invalid JSON) | `ci` fails, "Wait for CI to pass" fails; no merge |
| 5 | Opened by any other account | Skips with "Not created by bot" |

Example change for scenario 1:

```bash
git checkout -b test/valid-rule main
python3 - <<'EOF'
import json
p = "detections/engine/rule_status.json"
d = json.load(open(p))
d["rule_states"]["55555555-5555-4555-8555-555555555555"] = "beta"
json.dump(d, open(p, "w"), indent=2); open(p, "a").write("\n")
EOF
git commit -am "Add beta rule status" && git push -u origin HEAD
```

## Troubleshooting

- **Every run skips**: check the PR author is exactly `srsd-sigma-automation-pipeline[bot]`.
- **Workflow changes have no effect**: `pull_request_target` reads the workflow from the base branch, so changes only apply once they're on `main`.
- **403 in "Wait for CI to pass"**: the job needs `checks: read`.
- **Approve or merge fails**: check `AUTOMERGE_PAT` exists, isn't expired, and its account isn't the PR author.
