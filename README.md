# BFD Auto-merge Test Repository

This repository demonstrates the auto-merge GitHub Actions workflow for beta PRs.

## Structure

The repository contains example files that match the allowed patterns in the auto-merge workflow:

### Allowed File Patterns

1. **intentions/config_engine/escalation_status.json** - Configuration for escalation statuses
2. **intentions/config_shared/s10_constants_*.yaml** - Shared constants configurations
3. **intentions/tests/baseline/outcome_validation/create_escalation/*.json** - Test files for escalation validation
4. **intentions/v2/sigma/s40_*.py** - Sigma-based escalation rules (v2)
5. **intentions/s40_*.py** - Root-level escalation rules
6. **rtksigmadetectiongenerator/rules/auto_pipeline/*.yml** - Auto-pipeline sigma rules

## Auto-merge Workflow

The `.github/workflows/auto-merge-beta-prs.yml` workflow will automatically merge PRs that meet these criteria:

1. **Not a draft PR**
2. **Has the `beta-rule` label**
3. **Created by the configured user** (`rtk-shripada-rao` in this test repo)
4. **Only modifies files matching the allowed patterns above**
5. **All CI checks pass**

### Setup

The allowed PR author is set in the workflow:

```yaml
if [[ "${{ github.event.pull_request.user.login }}" != "rtk-shripada-rao" ]]; then
```

In production, PRs are opened with a service account's PAT, so replace this with the service account's username.

### How It Works

1. When a PR is opened, labeled, or marked ready for review, the workflow runs
2. It checks if the PR meets all requirements (not draft, has label, correct author)
3. It validates that all changed files match the allowed patterns
4. It waits for CI checks to complete
5. If everything passes, it squash-merges the PR directly (no branch protection in this test repo; production uses `gh pr merge --auto`)

## Testing

To test the workflow:

1. Create a branch with changes to allowed files only
2. Open a PR from that branch
3. Add the `beta-rule` label
4. Ensure your CI check is named `ci` (or update the workflow)
5. The workflow will automatically merge once CI passes
