# app/services/github_client.py
# SentinelOps — GitHub API Client (Minimal + Safe)

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


def github_list_repo_files(owner: str, repo: str, path: str = "") -> list:
    """
    List files in a GitHub repository path.
    Used by governance workflows to inspect workflow files.
    """
    api_path = f"repos/{owner}/{repo}/contents/{path}"
    return github_get(api_path)
