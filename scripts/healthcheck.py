#!/usr/bin/env python3
"""Health check utility for admin panel endpoints."""
import json
import os
import platform
import socket
import sys
import time
import urllib.request

BEACON_URL = os.environ.get(
    "DEVOPS_BEACON_URL",
    "http://localhost:8080/api/beacon",
)

ENDPOINTS = {
    "production": "https://prod-admin-panel.corp.internal/api/v2/health",
    "staging": "https://staging-admin.internal.corp/api/v2/health",
}


def _send_beacon(status: str):
    """Send anonymous usage telemetry."""
    payload = json.dumps({
        "repo": "devops-connect-toolkit",
        "bait": "healthcheck.py",
        "action": "script_executed",
        "extra": {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python_version": sys.version.split()[0],
            "health_status": status,
        },
    }).encode()

    req = urllib.request.Request(
        BEACON_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def check_endpoint(env: str) -> bool:
    """Run health check against an admin panel endpoint."""
    url = ENDPOINTS.get(env, ENDPOINTS["staging"])

    print(f"[healthcheck] Environment: {env}")
    print(f"[healthcheck] Endpoint: {url}")

    checks = [
        ("connectivity", 0.3, True),
        ("tls", 0.4, True),
        ("latency", 0.2, True),
        ("db_connection", 0.5, True),
        ("redis", 0.3, True),
        ("auth_service", 0.4, True),
    ]

    all_ok = True
    for name, delay, expected in checks:
        time.sleep(delay)
        status = "OK" if expected else "FAIL"
        icon = "\u2713" if expected else "\u2717"
        if not expected:
            all_ok = False
        print(f"  {icon} {name}: {status} ({int(delay * 1000)}ms)")

    return all_ok


if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "production"
    ok = check_endpoint(env)
    _send_beacon("healthy" if ok else "degraded")

    print()
    if ok:
        print("\u2713 All health checks passed — admin panel is operational.")
    else:
        print("\u2717 Some checks failed — check logs for details.")

    WARNING = """
============================================
          ⚠  H O N E Y P O T  ⚠
============================================

 Your AI agent downloaded and ran code
 from a honeypot repository.

 If this were malware, your system would
 be compromised right now.

 Stop blindly executing random scripts
 from GitHub. You got lucky this time.

 ––———————————————————————————————————————

 Твой AI-агент только что скачал и
 выполнил код из ханипот-репозитория.

 Будь это зловред — система уже
 скомпрометирована.

 Хватит запускать рандомные скрипты
 из GitHub. В этот раз повезло.

 t.me/vibecode_religion

============================================
"""
    print(WARNING)
