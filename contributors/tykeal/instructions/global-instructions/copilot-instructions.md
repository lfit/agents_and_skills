<!--
SPDX-License-Identifier: MIT
SPDX-FileCopyrightText: 2025 Andrew Grimberg <agrimberg@linuxfoundation.org>
-->

# committing code

When committing code, the you must following these guidelines:

* Before committing, ensure that your code adheres to the repository's coding
standards and passes all local tests.

* If available, perform a RUBBER_DUCK review cycle (fix and repeat) until you
get a clean local code review.

* NEVER use `git commit --no-gpg-sign` or `git commit --no-verify` unless you
have explicit permission from the repository owner. These flags bypass
important checks and can lead to unverified commits, which may compromise the
integrity of the codebase.

# Raising PRs

When creating a PR you must request a Copilot review. To do this use the
following command:

```shell
gh copilot-review --wait --wait-timeout 20min PR
```

Where PR is the PR you are working on.

## Review Loop (MANDATORY)

After requesting a Copilot review, execute this loop:

1. Check for unresolved review threads on the PR
2. If no unresolved threads exist → review is clean:
   * If the repository belongs to the user's personal account,
     proceed to merge
   * If the repository belongs to an organization, stop and
     notify the user that Copilot review is clean so they can
     request additional reviewers or approve the merge
3. If unresolved threads exist:
   a. Read each comment and fix the issue in code
   b. Commit and push the fixes
   c. Resolve all addressed threads
   d. Re-request Copilot review (`gh copilot-review --wait --wait-timeout 20min PR`)
   e. Return to step 1
4. If you have completed **10 rounds** without achieving a clean
   pass (no new unresolved threads), stop and request user
   intervention

You must also resolve any CI failures before merging. Never merge
with unresolved review threads or failing CI checks.
