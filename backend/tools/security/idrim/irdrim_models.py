# backend/tools/security/idrim/idrim_models.py

from typing import Dict, Any, List
from pydantic import BaseModel


class IDRIMSnapshot(BaseModel):
    roles: Dict[str, Any] = {}
    permissions: Dict[str, Any] = {}
    users: Dict[str, Any] = {}


class IDRIMBaseline(BaseModel):
    roles: Dict[str, Any] = {}
    permissions: Dict[str, Any] = {}
    users: Dict[str, Any] = {}


class IDRIMDriftSection(BaseModel):
    added: Dict[str, Any]
    removed: Dict[str, Any]
    changed: Dict[str, Any]


class IDRIMDriftEvent(BaseModel):
    event_type: str
    key: str
    details: Any


class IDRIMDriftResult(BaseModel):
    roles: IDRIMDriftSection
    permissions: IDRIMDriftSection
    users: IDRIMDriftSection


class IDRIMAnalysisResult(BaseModel):
    timestamp: str
    integrity_score: int
    summary: str
    drift_events: List[Dict[str, Any]]
    roles: Dict[str, Any]
    permissions: Dict[str, Any]
    users: Dict[str, Any]


class IDRIMRequest(BaseModel):
    source: str = "unknown"
    scope: str = "default"
    payload: Dict[str, Any] = {}


class IDRIMResult(BaseModel):
    success: bool
    details: Dict[str, Any]
