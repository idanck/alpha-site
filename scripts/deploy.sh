#!/usr/bin/env bash
# Publish index.html to the Cloudflare Worker that serves alpha.idanck.com.
#
# Usage:  scripts/deploy.sh
#
# Reads CLOUDFLARE_API_TOKEN and CF_ACCOUNT_ID from the environment. On the
# host that normally runs this, source the local credentials file first:
#   set -a; source "$CREDENTIALS_FILE"; set +a
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if [[ ! -f index.html ]]; then
  echo "error: index.html not found in $repo_root" >&2
  exit 1
fi

python3 scripts/build_worker.py

echo "verifying the live page..."
live_status=$(curl -fsS -o /tmp/alpha-site-live.html -w '%{http_code}' https://alpha.idanck.com/)
if [[ "$live_status" != "200" ]]; then
  echo "error: live page returned HTTP $live_status" >&2
  exit 1
fi
if cmp -s /tmp/alpha-site-live.html index.html; then
  echo "ok: live page is byte-identical to index.html"
else
  echo "warning: the live page differs from index.html (the edge cache may still be warm)" >&2
fi
