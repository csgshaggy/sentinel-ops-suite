from __future__ import annotations

from typing import List

from app.models.plugin_models import TimingBucketResponse


def get_timing_histogram() -> List[TimingBucketResponse]:
    """
    Return a static timing histogram for plugin execution.

    This is a placeholder implementation used by the dashboard and API
    until real timing metrics are wired into the backend. Each bucket
    represents a latency range and the number of plugin executions that
    fell into that range.

    Returns:
        List[TimingBucketResponse]: A list of timing buckets with counts.
    """
    return [
        TimingBucketResponse(bucket="0-50ms", count=12),
        TimingBucketResponse(bucket="50-100ms", count=8),
        TimingBucketResponse(bucket="100-200ms", count=4),
    ]
