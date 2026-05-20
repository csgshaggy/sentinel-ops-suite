import hashlib
from pathlib import Path


class FilesystemHashPlugin:
    """
    Collects SHA256 hashes of all files in the repository,
    excluding ignored directories.
    """

    name = "filesystem_hash"

    EXCLUDE_DIRS = {".git", ".venv", ".drift", "__pycache__"}

    def collect(self, root: Path) -> dict:
        data = {}
        for p in sorted(root.rglob("*")):
            if not p.is_file():
                continue

            # Skip excluded directories
            if any(ex in p.parts for ex in self.EXCLUDE_DIRS):
                continue

            data[str(p.relative_to(root))] = self._sha256_file(p)

        return data

    @staticmethod
    def _sha256_file(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
