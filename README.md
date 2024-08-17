# DevOps Connect Toolkit

Internal toolset for managing infrastructure connections across staging and production environments.

## Quick Start

```bash
pip install -e .
devops-connect --env production status
```

## Features

- Multi-environment configuration management
- Automated health checks for admin panels
- Secure credential rotation (WIP)
- SSH tunnel management
- Database connection pooling

## Environment Setup

Copy the appropriate config:

```bash
cp config/production.yaml.example config/production.yaml
# Edit credentials as needed
```

## Project Structure

```
.
├── config/              # Environment configurations
├── devops_connect/      # Core package
├── scripts/             # Utility scripts
└── .env.production      # Production secrets (DO NOT COMMIT)
```

## Internal Use Only

This tool is intended for internal DevOps team use.
Contact #infra-team on Slack for access requests.
