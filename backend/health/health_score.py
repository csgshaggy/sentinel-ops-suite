import psutil
import time

def compute_health_score():
    cpu = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    score = 100

    # CPU impact
    if cpu > 90:
        score -= 40
    elif cpu > 75:
        score -= 25
    elif cpu > 50:
        score -= 10

    # Memory impact
    if mem > 90:
        score -= 30
    elif mem > 75:
        score -= 15
    elif mem > 50:
        score -= 5

    # Disk impact
    if disk > 90:
        score -= 20
    elif disk > 75:
        score -= 10
    elif disk > 50:
        score -= 5

    return {
        "timestamp": int(time.time()),
        "cpu": cpu,
        "memory": mem,
        "disk": disk,
        "score": max(score, 0),
    }
