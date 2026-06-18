#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation
#
# Verify that every commit in a pull request is:
#   1. GPG-signed and verified by GitHub,
#   2. authored by the user who raised the pull request, and
#   3. accompanied by a DCO "Signed-off-by" trailer matching the author.
#
# Required environment variables:
#   GH_TOKEN            Token for the gh CLI (use ${{ github.token }}).
#   GITHUB_REPOSITORY   "owner/repo" (provided by GitHub Actions).
#   PR_NUMBER           Pull request number.
#   PR_AUTHOR           Login of the user who opened the pull request.

set -euo pipefail

: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY must be set}"
: "${PR_NUMBER:?PR_NUMBER must be set}"
: "${PR_AUTHOR:?PR_AUTHOR must be set}"

fail=0

commits_json="$(gh api --paginate "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/commits")"
count="$(jq 'length' <<<"${commits_json}")"

echo "Checking ${count} commit(s) in PR #${PR_NUMBER} (author: ${PR_AUTHOR})."

while IFS= read -r commit; do
  sha="$(jq -r '.sha' <<<"${commit}")"
  short="${sha:0:8}"
  verified="$(jq -r '.commit.verification.verified' <<<"${commit}")"
  reason="$(jq -r '.commit.verification.reason' <<<"${commit}")"
  signature="$(jq -r '.commit.verification.signature // ""' <<<"${commit}")"
  author_login="$(jq -r '.author.login // ""' <<<"${commit}")"
  author_name="$(jq -r '.commit.author.name' <<<"${commit}")"
  author_email="$(jq -r '.commit.author.email' <<<"${commit}")"
  message="$(jq -r '.commit.message' <<<"${commit}")"

  echo "::group::Commit ${short}"

  # 1. GPG-signed and verified by GitHub.
  if [[ "${verified}" != "true" ]]; then
    echo "::error::Commit ${short} is not a verified signed commit (reason: ${reason})."
    fail=1
  elif [[ "${signature}" != *"BEGIN PGP SIGNATURE"* ]]; then
    echo "::error::Commit ${short} is verified but not GPG-signed; only GPG signatures are accepted."
    fail=1
  else
    echo "Commit ${short}: GPG signature verified by GitHub."
  fi

  # 2. Authored by the user who raised the pull request.
  if [[ -z "${author_login}" ]]; then
    echo "::error::Commit ${short} has no linked GitHub account; cannot confirm author is '${PR_AUTHOR}'."
    fail=1
  elif [[ "${author_login}" != "${PR_AUTHOR}" ]]; then
    echo "::error::Commit ${short} authored by '${author_login}', but the PR author is '${PR_AUTHOR}'."
    fail=1
  else
    echo "Commit ${short}: authored by PR author '${PR_AUTHOR}'."
  fi

  # 3. DCO sign-off matching the commit author (must be a real trailer line,
  #    not an arbitrary substring elsewhere in the commit message).
  expected="Signed-off-by: ${author_name} <${author_email}>"
  if printf '%s\n' "${message}" | git interpret-trailers --parse |
    grep -qixF "${expected}"; then
    echo "Commit ${short}: DCO sign-off present."
  else
    echo "::error::Commit ${short} is missing a DCO sign-off matching the author: '${expected}'."
    fail=1
  fi

  echo "::endgroup::"
done < <(jq -c '.[]' <<<"${commits_json}")

if [[ "${fail}" -ne 0 ]]; then
  echo "::error::One or more commits failed the signing, authorship, or DCO checks."
  exit 1
fi

echo "All commits are GPG-verified, authored by the PR author, and DCO signed-off."
