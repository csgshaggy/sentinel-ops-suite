from pydantic import BaseModel
from typing import Optional, Dict, Any


class IDRIMRequest(BaseModel):
    """Incoming request payload for IDRIM analysis."""
    source: str
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class IDRIMResult(BaseModel):
    """Standardized output from IDRIMEngine."""
    status: str
    score: float
    details: Dict[str, Any]
    warnings: Optional[list[str]] = None
