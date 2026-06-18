<!--
SPDX-License-Identifier: MIT
SPDX-FileCopyrightText: 2025 Andrew Grimberg <agrimberg@linuxfoundation.org>
-->

# pm-agent

## Overview

`pm-agent` is a full-lifecycle project manager and lead developer agent. It
owns a change from request through specification, implementation, testing, PR
creation, review resolution, and merge, operating with minimal user
intervention. It targets repositories with strict commit conventions,
pre-commit hooks, and branch protection.

## Target tool

GitHub Copilot CLI custom agent. The definition lives in
[`pm_agent.md`](./pm_agent.md) and uses Copilot agent frontmatter
(`description`, `applyTo`).

## Usage

1. Copy [`pm_agent.md`](./pm_agent.md) into your Copilot agents directory:

   ```shell
   cp pm_agent.md ~/.copilot/agents/pm_agent.md
   ```

2. Invoke the `pm_agent` custom agent from the Copilot CLI and pass the issue
   number or task description as input.

## Configuration

- Accepts free-form input (an issue reference or a task description). With no
  input, the agent asks what you need.
- Assumes the target repository provides its own commit conventions, hooks, and
  CI; the agent adapts to them rather than imposing new ones.

## Examples

- "Resolve issue #42" — the agent reads the issue, plans, implements on a
  worktree branch, validates against CI, resolves review threads, and merges.

## Maintainer

- Author: `tykeal`
- Questions or issues: open an issue and mention the author.
