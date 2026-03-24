from pydantic import BaseModel


class PluginResponse(BaseModel):
    id: str
    name: str
    category: str
    status: str
    avgDurationMs: int
    lastRunAt: str | None


class TimingBucketResponse(BaseModel):
    bucket: str
    count: int
