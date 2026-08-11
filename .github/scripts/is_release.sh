#!/bin/sh

# This script checks if the current commit contains changesets that release something.
#
# An empty changeset (`changeset add --empty`) is a marker that a change needs no
# release, so it must not count: it would start a release that publishes nothing,
# and the version step's only effect — deleting the marker — is a commit the
# publish workflow deliberately does not push when no tags were created. The
# marker would survive on the branch and re-trigger a no-op release, with Slack
# notifications, on every later push. It is instead consumed by the next real
# release.

set -eu

CHANGES=$(node -e "require('@changesets/read').default(process.cwd()).then(result => console.log(result.some(changeset => changeset.releases.length > 0)))")

echo "${CHANGES}"
