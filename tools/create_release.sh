#!/usr/bin/env bash
# Usage: ./create_release.sh <tag> <name> <release_notes_file> [draft] [prerelease]
# Requires: GITHUB_TOKEN environment variable with repo write permissions

set -euo pipefail

TAG="$1"
NAME="$2"
RELEASE_NOTES_FILE="$3"
DRAFT=${4:-true}
PRERELEASE=${5:-false}

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "GITHUB_TOKEN is required"
  exit 1
fi

OWNER_REPO="hedeya/arxml-editor"
API_URL="https://api.github.com/repos/${OWNER_REPO}/releases"

BODY=$(jq -Rs . < "${RELEASE_NOTES_FILE}")

DATA=$(jq -n --arg tag "${TAG}" --arg name "${NAME}" --arg body "$BODY" --argjson draft $DRAFT --argjson prerelease $PRERELEASE '{tag_name: $tag, name: $name, body: $body, draft: $draft, prerelease: $prerelease}')

curl -sSL -X POST "$API_URL" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$DATA"

echo "Release request submitted (check GitHub for status)."