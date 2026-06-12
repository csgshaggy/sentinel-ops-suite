# app/services/github_client.py
# SentinelOps — GitHub API Client (SYNC Version, Final)

import os
import requests
from typing import Optional


GITHUB_API_BASE = "https://api.github.com"


def _get_token() -> Optional[str]:
    """
    Retrieve GitHub token from environment.
    Governance features may be disabled if missing.
    """
    return os.getenv("GITHUB_TOKEN")


def github_get(path: str) -> dict:
    """
    Perform a GET request to the GitHub API.
    Returns JSON or raises an exception on failure.
    """
    url = f"{GITHUB_API_BASE}/{path.lstrip('/')}"
    token = _get_token()

    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(
            f"GitHub API GET {url} failed: {response.status_code} {response.text}"
        )

    return response.json()


def github_post(path: str, payload: dict) -> None:
    """
    Perform a POST request to the GitHub API.
    Used for workflow dispatch.
    """
    url = f"{GITHUB_API_BASE}/{path.lstrip('/')}"
    token = _get_token()

    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(url, json=payload, headers=headers, timeout=10)

    if response.status_code not in (200, 201, 204):
        raise RuntimeError(
            f"GitHub API POST {url} failed: {response.status_code} {response.text}"
        )


def github_list_repo_files(owner: str, repo: str, path: str = "") -> list:
    """
    List files in a GitHub repository path.
    Used by governance workflows to inspect workflow files.
    """
    api_path = f"repos/{owner}/{repo}/contents/{path}"
    return github_get(api_path)


class GitHubClient:
    """
    Class-based wrapper for GitHub API operations.
    This satisfies imports in app.main and routers.
    """

    # ------------------------------
    # File listing (already existed)
    # ------------------------------
    def list_repo_files(self, owner: str, repo: str, path: str = "") -> list:
        return github_list_repo_files(owner, repo, path)

    # ------------------------------
    # Trigger workflow dispatch
    # ------------------------------
    def trigger_workflow_dispatch(
        self,
        repo_owner: str,
        repo_name: str,
        workflow_file: str,
        ref: str,
    ) -> None:
        api_path = (
            f"repos/{repo_owner}/{repo_name}/actions/workflows/"
            f"{workflow_file}/dispatches"
        )
        github_post(api_path, {"ref": ref})

    # ------------------------------
    # List workflows in a repo
    # ------------------------------
    def list_workflows(self, repo_owner: str, repo_name: str) -> list:
        api_path = f"repos/{repo_owner}/{repo_name}/actions/workflows"
        data = github_get(api_path)
        return data.get("workflows", [])

    # ------------------------------
    # List workflow runs
    # ------------------------------
    def list_workflow_runs(self, repo_owner: str, repo_name: str, workflow_id: int) -> list:
        api_path = (
            f"repos/{repo_owner}/{repo_name}/actions/workflows/"
            f"{workflow_id}/runs"
        )
        data = github_get(api_path)
        return data.get("workflow_runs", [])

    # ------------------------------
    # Get a single workflow run
    # ------------------------------
    def get_workflow_run(self, repo_owner: str, repo_name: str, run_id: int) -> dict:
        api_path = (
            f"repos/{repo_owner}/{repo_name}/actions/runs/{run_id}"
        )
        return github_get(api_path)
