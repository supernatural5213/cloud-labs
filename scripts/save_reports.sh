#!/usr/bin/env bash
# Сохранение отчётов CI в ветку ci-reports: <workflow>/<run_id>/
set -u
DIR="$1"; shift
REPO_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
rm -rf /tmp/rep
if ! git clone -q --depth 1 --branch ci-reports "$REPO_URL" /tmp/rep 2>/dev/null; then
  git init -q /tmp/rep && git -C /tmp/rep checkout -q -b ci-reports && git -C /tmp/rep remote add origin "$REPO_URL"
fi
mkdir -p "/tmp/rep/$DIR/$GITHUB_RUN_ID"
for f in "$@"; do [ -e "$f" ] && cp -r "$f" "/tmp/rep/$DIR/$GITHUB_RUN_ID/"; done
cd /tmp/rep
git config user.name "github-actions[bot]"; git config user.email "github-actions[bot]@users.noreply.github.com"
git add -A && git commit -q -m "$DIR: run $GITHUB_RUN_ID ($GITHUB_SHA)"
for i in 1 2 3 4 5; do
  git push -q origin ci-reports && exit 0
  git pull -q --rebase origin ci-reports; sleep $((i * 2))
done
exit 1
