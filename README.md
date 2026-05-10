# DevOps Connect Toolkit

Internal toolset for managing infrastructure connections across staging and production environments.

## Requirements

- Python 3.9+
- Access to corp internal network (VPN or bastion)

## Quick Start

```bash
pip install -e .
devops-connect --env production status
```

## Features

- Multi-environment configuration management
- Automated health checks for admin panels
- Credential rotation support
- SSH tunnel management
- Database connection pooling

## Configuration

Environment configs live in `config/`. Refer to the respective `.yaml` files for settings.

## Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| `connect_admin.sh` | Linux/macOS | Admin panel connection |
| `connect_admin.bat` | Windows | Batch launcher |
| `connect_admin.ps1` | Windows | PowerShell connector |
| `healthcheck.py` | Cross-platform | Endpoint health monitoring |

## Support

`.env.production` contains production credentials.
Contact #infra-team on Slack for access requests.
