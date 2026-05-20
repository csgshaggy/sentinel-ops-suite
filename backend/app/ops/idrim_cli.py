# app/ops/idrim_cli.py

import json
import click
import requests
from pathlib import Path

API = "http://localhost:8000"
DATA_DIR = Path("data/idrim")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2))
    click.echo(f"Saved → {path}")


@click.group()
def cli():
    """IDRIM Operator CLI"""
    pass


@cli.command()
def baseline():
    click.echo("→ Generating baseline...")
    res = requests.post(f"{API}/idrim/baseline", json={
        "roles": {},
        "permissions": {},
        "users": {},
    })
    write_json(DATA_DIR / "baseline.json", res.json())


@cli.command()
def scan():
    click.echo("→ Running snapshot scan...")
    res = requests.post(f"{API}/idrim/analysis", json={
        "roles": {},
        "permissions": {},
        "users": {},
    })
    write_json(DATA_DIR / "snapshot.json", res.json())


@cli.command()
def diff():
    click.echo("→ Generating diff...")
    snapshot_path = DATA_DIR / "snapshot.json"
    if not snapshot_path.exists():
        click.echo("Snapshot missing. Run: idrim scan")
        return
    snapshot = json.loads(snapshot_path.read_text())
    res = requests.post(f"{API}/idrim/diff", json=snapshot)
    write_json(DATA_DIR / "diff.json", res.json())


@cli.command()
@click.option("--provider", default="aws", help="IAM provider name")
def ingest(provider):
    click.echo(f"→ Fetching IAM data from provider: {provider}")
    res = requests.get(f"{API}/iam/{provider}")
    write_json(DATA_DIR / "ingest.json", res.json())


if __name__ == "__main__":
    cli()
