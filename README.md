# Auto-merge Test Repository

Test bed for a GitHub Actions workflow that approves and merges automation-generated detection PRs.

## How it works

`.github/workflows/auto-merge-beta-prs.yml` runs on `pull_request_target` (opened, labeled, ready for review), so the workflow always comes from the base branch and a PR can't change the rules it's judged by.

1. **Gate**: skip if the PR is a draft or wasn't opened by `srsd-sigma-automation-pipeline[bot]` (the GitHub App).
2. **Path allowlist**: fail if the PR touches any file outside the allowed patterns below.
3. **Approve**: the service account approves the PR.
4. **Enable auto-merge**: `gh pr merge --auto --squash`. GitHub merges once the branch ruleset's required checks and approval are satisfied.

Steps 3–4 use the `AUTOMERGE_PAT` secret (the service account's PAT). The PR author can't approve its own PR, which is why the app opens it and the service account approves it. A PAT is used instead of `GITHUB_TOKEN` because merges made with `GITHUB_TOKEN` don't trigger `push` workflows on the base branch.

## Allowed file patterns

```
detections/engine/rule_status.json
detections/shared/constants_autopipeline_*.yaml
detections/tests/rule_autopipeline_*/**/*.json
detections/v2/rule_autopipeline_*.py
detections/rule_autopipeline_*.py
generator/rules/auto_pipeline/**/*.yml
```

## Repo settings this relies on

- **Settings → General → Allow auto-merge** is on.
- A branch ruleset on `main` requiring a PR with 1 approval, dismissal of stale approvals on push, approval of the most recent push, and the `ci` status check.

`--auto` only waits for checks marked required in the ruleset.

See [TESTING.md](TESTING.md) for test scenarios.
