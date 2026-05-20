# app/providers/iam/aws.py

import boto3
from .base import IAMProvider


class AWSIAMProvider(IAMProvider):
    def __init__(self):
        self.iam = boto3.client("iam")

    def fetch_roles(self):
        roles = self.iam.list_roles()["Roles"]
        return {r["RoleName"]: r for r in roles}

    def fetch_permissions(self):
        policies = self.iam.list_policies(Scope="Local")["Policies"]
        return {p["PolicyName"]: p for p in policies}

    def fetch_users(self):
        users = self.iam.list_users()["Users"]
        return {u["UserName"]: u for u in users}
