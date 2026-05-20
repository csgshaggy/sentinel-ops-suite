# app/providers/iam/base.py

from abc import ABC, abstractmethod


class IAMProvider(ABC):
    @abstractmethod
    def fetch_roles(self):
        pass

    @abstractmethod
    def fetch_permissions(self):
        pass

    @abstractmethod
    def fetch_users(self):
        pass

    def fetch_all(self):
        return {
            "roles": self.fetch_roles(),
            "permissions": self.fetch_permissions(),
            "users": self.fetch_users(),
        }
