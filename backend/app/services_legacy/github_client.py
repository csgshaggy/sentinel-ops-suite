class GitHubClient:
    def __init__(self, token: str):
        self.token = token

    async def trigger_workflow_dispatch(self, repo_owner: str, repo_name: str, workflow_file: str, ref: str):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_file}/dispatches"

        payload = {"ref": ref}

        async with httpx.AsyncClient() as client:
            await client.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {self.token}",
                         "Accept": "application/vnd.github+json"}
            )
