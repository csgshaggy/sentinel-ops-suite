# app/providers/iam/registry.py

from .aws import AWSIAMProvider

PROVIDERS = {
    "aws": AWSIAMProvider,
}


def get_provider(name: str):
    if name not in PROVIDERS:
        raise ValueError(f"Unknown IAM provider: {name}")
    return PROVIDERS[name]()
