# wait-for-git-commit-status-action

This action waits for a commit status to succeed and it also returns the JSON of the commit status. It uses the Github API [Get the combined status for a specific reference](https://docs.github.com/en/rest/commits/statuses?apiVersion=2022-11-28#get-the-combined-status-for-a-specific-reference) to fetch the commit statuses and then checks the status of the specified status `context`.

## Usage:

### Example
```
jobs:
  example_case:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run the action
        id: test_action
        uses: mfaizanse/github-action/wait-for-git-commit-status-action@1.0.0
        with:
          context: "<CONTEXT_NAME>"
          commit_ref: "<COMMIT_REF | SHA>"
          timeout: <TIME_IN_MILLISECONDS>
        env:
          GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
          GITHUB_OWNER: "<OWNER>"
          GITHUB_REPO: "<REPO>"
      - name: Use the results
        run: |
          echo "${{ steps.test_action.outputs.state }}"
          echo "${{ steps.test_action.outputs.json }}"
```

### Required Inputs

- **`context`**: The context value of the status.
- **`commit_ref`**: The commit reference. Can be a commit SHA, branch name (`heads/BRANCH_NAME`), or tag name (`tags/TAG_NAME`). ([Reference](https://docs.github.com/en/rest/commits/statuses?apiVersion=2022-11-28#get-the-combined-status-for-a-specific-reference))
- **`timeout`**: The time (Milliseconds) to wait for the status to succeed.

### Required ENV variables

- **`GITHUB_TOKEN`**: Token to authenticate with Github API. e.g. `${{ secrets.GITHUB_TOKEN }}`.
- **`GITHUB_OWNER`**: The account owner of the repository. The name is not case sensitive.
- **`GITHUB_REPO`**: The name of the repository without the .git extension. The name is not case sensitive.

### Outputs

- **`state`**: The state value of the retrieved status.
- **`json`**: The stringified JSON of the retrieved status object.