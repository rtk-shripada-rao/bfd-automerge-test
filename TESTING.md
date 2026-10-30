# Testing the Auto-merge Workflow

## Prerequisites

- The `bfd-automerge-test-bot` GitHub App is installed on this repo; test PRs must be opened by it. Production uses `26-srsd-sigma-automation-pipeline`.
- Repo secret `AUTOMERGE_PAT`: a PAT for a service account (not the app) with **Contents** and **Pull requests** read/write on this repo.

## Scenarios

| # | PR | Expected |
|---|---|---|
| 1 | Opened by the app, only changes `detections/engine/rule_status.json` | CI passes, PR is approved and merged |
| 2 | Opened by the app, also adds `unauthorized_file.txt` | "Check files changed" fails and lists the file; no merge |
| 3 | Opened by the app as a draft | Skips with a "draft=true" notice; marking it ready for review re-runs CI, then it merges |
| 4 | Opened by the app, breaks `rule_status.json` (invalid JSON) | `ci` fails, so the auto-merge job is skipped; no approval or merge |
| 5 | Opened by any other account | Job is skipped (CI run not started by the app) |
| 6 | Opened by the app, sets a rule to `"ga"` in `rule_status.json` | "Check files changed" fails with "GA auto-merging is disabled"; no approval or merge |
| 7 | Someone other than the app pushes to an open bot PR | Job is skipped; the push does not get auto-approved |

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

- **Every run skips**: check the PR author is exactly `bfd-automerge-test-bot[bot]`.
- **Workflow changes have no effect**: `workflow_run` reads the workflow from the default branch, so changes only apply once they're on `main`.
- **Nothing happens after CI**: auto-merge runs show in the Actions tab, not on the PR. Check that `workflows: [CI]` still matches `ci.yml`'s `name:`.
- **Approve or merge fails**: check `AUTOMERGE_PAT` exists, isn't expired, and its account isn't the PR author.
- **Merge step fails after checks pass**: the PR merge box lists what's still blocking (usually the approval); a "head commit" error means commits were pushed after the run started.
- **Need to push to `main` directly**: the ruleset blocks it; set the ruleset's enforcement to Disabled, push, then re-enable it.
