# Testing the Auto-merge Workflow

## Prerequisites

1. The allowed PR author in `.github/workflows/auto-merge-beta-prs.yml` is `rtk-shripada-rao`. Open test PRs with those credentials (in production this becomes the service account's username).

2. Create a `beta-rule` label in your GitHub repository:
   - Go to Issues → Labels → New Label
   - Name: `beta-rule`
   - Color: (your choice)
   - Description: "Enables auto-merge for beta rules"

## Test Scenarios

### ✅ Scenario 1: Valid PR (Should Auto-merge)

1. Create a new branch:
   ```bash
   git checkout -b test/valid-beta-rule
   ```

2. Modify an allowed file:
   ```bash
   # Edit intentions/config_engine/escalation_status.json
   # Add a new entry to the escalation_states
   ```

3. Commit and push:
   ```bash
   git add intentions/config_engine/escalation_status.json
   git commit -m "Update escalation status for new rule"
   git push origin test/valid-beta-rule
   ```

4. Create PR:
   - Open PR to main/master branch
   - Add the `beta-rule` label
   - Ensure the PR is created by `rtk-shripada-rao`
   - Wait for CI to complete

**Expected**: PR should auto-merge after CI passes

### ❌ Scenario 2: Invalid File Path (Should Fail)

1. Create a new branch:
   ```bash
   git checkout -b test/invalid-path
   ```

2. Create a file outside allowed patterns:
   ```bash
   echo "test" > unauthorized_file.txt
   git add unauthorized_file.txt
   git commit -m "Add unauthorized file"
   git push origin test/invalid-path
   ```

3. Create PR with `beta-rule` label

**Expected**: Workflow should fail with message about files outside allowed paths

### ❌ Scenario 3: Missing Label (Should Skip)

1. Create a valid PR (like Scenario 1)
2. Don't add the `beta-rule` label

**Expected**: Workflow should skip with message "Missing beta-rule label"

### ❌ Scenario 4: Draft PR (Should Skip)

1. Create a valid PR (like Scenario 1)
2. Create it as a Draft PR
3. Add the `beta-rule` label

**Expected**: Workflow should skip with message "PR is draft"

### ❌ Scenario 5: Wrong User (Should Skip)

1. Create a valid PR (like Scenario 1) from an account other than `rtk-shripada-rao`
2. Add the `beta-rule` label

**Expected**: Workflow should skip with message "Not created by bot"

## Allowed File Patterns Reference

Files that can be auto-merged:

```
intentions/config_engine/escalation_status.json
intentions/config_shared/s10_constants_*.yaml
intentions/tests/baseline/outcome_validation/create_escalation/**/*.json
intentions/v2/sigma/s40_*.py
intentions/s40_*.py
rtksigmadetectiongenerator/rules/auto_pipeline/**/*.yml
```

## Monitoring

View workflow runs:
```
GitHub Repo → Actions → Auto-merge Beta PRs
```

Check workflow logs to see:
- Which validation step failed
- Reason for skipping
- File validation results
- CI status

## Troubleshooting

### Auto-merge doesn't trigger
- Check if the PR has the `beta-rule` label
- Verify the PR author is `rtk-shripada-rao`
- Ensure PR is not in draft status

### File validation fails
- Review the workflow logs for the list of invalid files
- Ensure all changed files match one of the allowed patterns
- Use regex tester to verify pattern matching

### CI doesn't complete
- Check the CI workflow configuration (`.github/workflows/ci.yml`)
- Ensure the check name is `ci` (matches the workflow job name)
- Review CI logs for failures

### Auto-merge enabled but PR not merging
- Check if there are merge conflicts
- Ensure the workflow has `contents: write` and `pull-requests: write` permissions
