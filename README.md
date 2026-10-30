# Auto-merge Test Repository

Test bed for a GitHub Actions workflow that approves and merges automation-generated detection PRs.

## How it works

`.github/workflows/auto-merge-beta-prs.yml` runs on `pull_request_target` (opened, labeled, ready for review), so the workflow always comes from the base branch and a PR can't change the rules it's judged by.

1. **Gate**: the job is skipped if the PR is a draft or wasn't opened by `bfd-automerge-test-bot[bot]` (the GitHub App). Production uses `26-srsd-sigma-automation-pipeline[bot]`.
2. **Path allowlist**: fail if the PR touches any file outside the allowed patterns below, or if it sets a rule to `"ga"` in `rule_status.json` (GA auto-merging is disabled).
3. **Wait for checks**: wait until the ruleset's required checks register, then `gh pr checks --required --watch --fail-fast`. A failing check stops the run before approval.
4. **Approve**: the service account approves the PR.
5. **Merge**: `gh pr merge --squash --match-head-commit`. Repo auto-merge is off, so the workflow merges directly.

`check_suite` can't be used to run after CI instead: GitHub doesn't trigger workflows from check suites created by GitHub Actions.

Steps 3–5 use the `AUTOMERGE_PAT` secret (the service account's PAT). The PR author can't approve its own PR, which is why the app opens it and the service account approves it. A PAT is used instead of `GITHUB_TOKEN` because merges made with `GITHUB_TOKEN` don't trigger `push` workflows on the base branch.

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

- **Settings → General → Allow auto-merge** is off (the workflow merges directly).
- A branch ruleset on `main` requiring a PR with 1 approval, dismissal of stale approvals on push, approval of the most recent push, and the `ci` status check.

The merge step only waits for checks marked required in the ruleset.

See [TESTING.md](TESTING.md) for test scenarios.
