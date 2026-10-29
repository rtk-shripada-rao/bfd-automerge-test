# Auto-merge Test Repository

Test bed for a GitHub Actions workflow that approves and merges automation-generated detection PRs.

## How it works

`.github/workflows/auto-merge-beta-prs.yml` runs on `pull_request_target` (opened, labeled, ready for review), so the workflow always comes from the base branch and a PR can't change the rules it's judged by.

1. **Gate**: skip if the PR is a draft or wasn't opened by `srsd-sigma-automation-pipeline[bot]` (the GitHub App).
2. **Path allowlist**: fail if the PR touches any file outside the allowed patterns below.
3. **Wait for CI**: poll until the `ci` check passes (test repo only; see below).
4. **Approve**: the service account approves the PR.
5. **Merge**: the service account squash-merges the PR.

Steps 4–5 use the `AUTOMERGE_PAT` secret (the service account's PAT). The PR author can't approve its own PR, which is why the app opens it and the service account approves it. A PAT is used instead of `GITHUB_TOKEN` because merges made with `GITHUB_TOKEN` don't trigger `push` workflows on the base branch.

## Allowed file patterns

```
detections/engine/rule_status.json
detections/shared/constants_autopipeline_*.yaml
detections/tests/rule_autopipeline_*/**/*.json
detections/v2/rule_autopipeline_*.py
detections/rule_autopipeline_*.py
generator/rules/auto_pipeline/**/*.yml
```

## Test repo vs production

| | Test repo | Production |
|---|---|---|
| Branch protection | None | Required checks + 1 approval |
| Wait for CI step | Waits on `ci` | Remove; `--auto` waits for all required checks |
| Merge | `gh pr merge --squash` | `gh pr merge --auto --squash` |

Production also needs **Settings → General → Allow auto-merge** and **Dismiss stale approvals when new commits are pushed** in the branch rules.

See [TESTING.md](TESTING.md) for test scenarios.
