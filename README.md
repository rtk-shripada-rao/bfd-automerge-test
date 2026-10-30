# Auto-merge Test Repository

Test bed for a GitHub Actions workflow that approves and merges automation-generated detection PRs.

## How it works

`.github/workflows/auto-merge-beta-prs.yml` runs on `workflow_run` when the `CI` workflow completes. `workflow_run` always uses the copy on the default branch, so a PR can't change the rules it's judged by. The run never checks out PR code.

1. **Gate**: the job is skipped unless CI succeeded on a `pull_request` run started by `bfd-automerge-test-bot[bot]` (the GitHub App opening the PR or pushing to it). Production uses `26-srsd-sigma-automation-pipeline[bot]`.
2. **PR checks**: look up the PR. Skip with a notice if it's closed, a draft, opened by someone else, or has moved past the commit CI ran on (the newer commit's CI run triggers a fresh run).
3. **Path allowlist**: fail if the PR touches any file outside the allowed patterns below, or sets a rule to `"ga"` in `rule_status.json` (GA auto-merging is disabled).
4. **Approve**: the service account approves the PR.
5. **Merge**: `gh pr merge --squash --match-head-commit` with the commit CI ran on. Repo auto-merge is off, so the workflow merges directly.

CI also runs on `ready_for_review`, so a draft is picked up once it's marked ready. The workflow name in `workflows: [CI]` must match `ci.yml`'s `name:`. These runs happen on the default branch, so they show up in the Actions tab rather than in the PR's checks.

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

## Repo settings this relies on

- **Settings → General → Allow auto-merge** is off (the workflow merges directly).
- A branch ruleset on `main` requiring a PR with 1 approval, dismissal of stale approvals on push, approval of the most recent push, and the `ci` status check.

The merge step only waits for checks marked required in the ruleset.

See [TESTING.md](TESTING.md) for test scenarios.
