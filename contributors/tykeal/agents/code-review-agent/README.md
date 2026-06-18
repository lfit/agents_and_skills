<!--
SPDX-License-Identifier: MIT
SPDX-FileCopyrightText: 2025 Andrew Grimberg <agrimberg@linuxfoundation.org>
-->

# code-review-agent

## Overview

`code-review-agent` is a generic, language-agnostic pull request reviewer. It
acts as a senior maintainer and performs rigorous, constructive, high-signal
reviews for any project, adapting to the repository's stack, conventions, and
tooling.

## Target tool

GitHub Copilot CLI custom agent. The definition lives in
[`code_review_agent.md`](./code_review_agent.md) and uses Copilot agent
frontmatter (`description`, `applyTo`).

## Usage

1. Copy [`code_review_agent.md`](./code_review_agent.md) into your Copilot
   agents directory:

   ```shell
   cp code_review_agent.md ~/.copilot/agents/code_review_agent.md
   ```

2. Invoke the `code_review_agent` custom agent from the Copilot CLI on the
   change set or pull request you want reviewed.

## Configuration

None. The agent adapts to the target repository's language, conventions, and
tooling rather than requiring its own configuration.

## Examples

- "Review my staged changes" — the agent produces a structured, high-signal
  review focused on correctness and real defects.

## Maintainer

- Author: `tykeal`
- Questions or issues: open an issue and mention the author.
