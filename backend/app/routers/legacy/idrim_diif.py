# app/routers/idrim_diff.py

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/idrim", tags=["IDRIM-Diff"])

def get_service():
    return IDRIMService(storage_path="data/idrim")


def diff_dict(a, b):
    added = {k: b[k] for k in b if k not in a}
    removed = {k: a[k] for k in a if k not in b}
    changed = {
        k: {"before": a[k], "after": b[k]}
        for k in a
        if k in b and a[k] != b[k]
    }
    return {"added": added, "removed": removed, "changed": changed}


@router.post("/diff")
async def idrim_diff(snapshot: dict, service: IDRIMService = Depends(get_service)):
    baseline = service.load_baseline()
    return {
        "roles": diff_dict(baseline.get("roles", {}), snapshot.get("roles", {})),
        "permissions": diff_dict(
            baseline.get("permissions", {}), snapshot.get("permissions", {})
        ),
        "users": diff_dict(baseline.get("users", {}), snapshot.get("users", {})),
    }
from tools.security.idrim.idrim_service import IDRIMService
