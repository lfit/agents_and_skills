<!--
SPDX-License-Identifier: Apache-2.0
SPDX-FileCopyrightText: 2025 The Linux Foundation
-->

# Agents and Skills

A shared, tool-agnostic collection of AI **agents** and **skills** built by the
team. Each entry is self-contained, documented, and owned by the contributor
who created it, so anyone can discover, reuse, and improve them.

## Overview

- **Agents** are higher-level personas or assistants with a defined role,
  instructions, and (optionally) tool configuration.
- **Skills** are focused, reusable procedures or instructions that a person or
  an agent can invoke to complete a specific task.
- **Instructions** are standing directives (global or per-repository) that
  shape how a tool behaves across sessions.

Entries may target any tool or runtime (GitHub Copilot, Claude, Cursor, MCP,
or a generic/portable prompt). The target tool is recorded in each entry's
metadata.

## Repository layout

The repository is organized **by contributor**, then by **kind**, then by
**entry**. Each entry lives in its own folder with a definition, a README, and
a `metadata.yaml`.

```text
contributors/
└── <your-handle>/
    ├── agents/
    │   └── <agent-name>/
    │       ├── metadata.yaml   # structured metadata (see Conventions)
    │       ├── README.md       # how to use this agent
    │       └── agent.md        # the agent definition
    ├── skills/
    │   └── <skill-name>/
    │       ├── metadata.yaml
    │       ├── README.md
    │       └── skill.md
    └── instructions/
        └── <instruction-name>/
            ├── metadata.yaml
            ├── README.md
            └── instructions.md

templates/      # copy-ready starting points for each kind of entry
scripts/        # automation (index generation, PR signing checks)
.github/        # CI workflows
```

Reserved top-level names (`contributors/`, `templates/`, `scripts/`,
`.github/`, `LICENSES/`) are not contributor handles. See
[`contributors/_example/`](contributors/_example/) for a worked example.

## Usage

To use an agent, skill, or instruction set:

1. Browse the [catalog index](#catalog-index) or the `contributors/` tree.
2. Open the entry's folder and read its `README.md`.
3. Load the definition file (`agent.md`, `skill.md`, or `instructions.md`)
   into the target tool named in the entry's `metadata.yaml`.

## Contributing

1. Copy the matching folder from [`templates/`](templates/):
   - `templates/agent/` for an agent,
   - `templates/skill/` for a skill, or
   - `templates/instructions/` for an instruction set.
2. Place it under
   `contributors/<your-handle>/<agents|skills|instructions>/<entry-name>/`.
3. Fill in `metadata.yaml`, the entry `README.md`, and the definition file.
4. Regenerate the catalog index:

   ```shell
   python scripts/generate_index.py
   ```

5. Commit your work with a **GPG-signed** commit that includes a DCO
   `Signed-off-by` trailer (see [Commit signing](#commit-signing)).
6. Open a pull request.

### Conventions

- **Folder names**: lowercase `kebab-case` (for example, `release-notes-agent`).
- **One entry per folder**, fully self-contained — keep all tool-specific
  assets inside the entry folder.
- **`metadata.yaml` fields** (all required unless noted):

  | Field         | Description                                              |
  | ------------- | -------------------------------------------------------- |
  | `name`        | Human-readable name of the entry.                        |
  | `description` | One- or two-sentence summary of purpose and use.         |
  | `author`      | GitHub handle (or team) that owns the entry.             |
  | `tool`        | Target tool: `copilot`, `claude`, `cursor`, `generic`, … |
  | `kind`        | `agent`, `skill`, or `instructions`.                     |
  | `tags`        | List of discovery tags/categories.                       |
  | `version`     | Semantic version of the entry definition.                |
  | `license`     | SPDX identifier (defaults to `Apache-2.0`).              |

- Every file carries SPDX headers; the repository is [REUSE][reuse]-compliant
  and validated by `pre-commit`.

## Commit signing

Every commit in a pull request must be:

1. **GPG-signed and verified by GitHub** — the signing key must be registered
   on the author's GitHub account so the commit shows as *Verified*.
2. **Authored by the person who opened the pull request.**
3. **DCO signed-off** — include a trailer matching the commit author:

   ```text
   Signed-off-by: Your Name <you@example.com>
   ```

These rules are enforced automatically by the
[`Verify commit signing`](.github/workflows/verify-signing.yaml) workflow,
which uses [`scripts/verify-pr-signing.sh`](scripts/verify-pr-signing.sh).

To configure signing locally:

```shell
git config --global user.signingkey <your-gpg-key-id>
git config --global commit.gpgsign true
git commit --signoff --gpg-sign -m "Your message"
```

Upload your public GPG key to GitHub under
**Settings → SSH and GPG keys** so GitHub can verify your signatures.

## Catalog index

This section is generated from each entry's `metadata.yaml` by
[`scripts/generate_index.py`](scripts/generate_index.py). Do not edit it by
hand; run the script and commit the result.

<!-- BEGIN INDEX -->

### _example

| Name | Kind | Tool | Description | Tags | Version |
| --- | --- | --- | --- | --- | --- |
| [hello-agent](contributors/_example/agents/hello-agent) | agent | generic | Example agent that greets the user and explains how shared agents are structured in this repository. | example, getting-started | 0.1.0 |
| [hello-skill](contributors/_example/skills/hello-skill) | skill | generic | Example skill that summarizes the conventions for adding a new entry to the shared agents and skills repository. | example, getting-started | 0.1.0 |

### tykeal

| Name | Kind | Tool | Description | Tags | Version |
| --- | --- | --- | --- | --- | --- |
| [code-review-agent](contributors/tykeal/agents/code-review-agent) | agent | copilot | Generic, language-agnostic pull request review agent. Performs rigorous, structured, high-signal code reviews for any repository, adapting to each project's stack, conventions, and tooling. | code-review, pull-request, quality, automation | 1.0.0 |
| [pm-agent](contributors/tykeal/agents/pm-agent) | agent | copilot | Project manager agent that drives the full development lifecycle: spec authoring, implementation planning, coding, testing, PR review, and merge. Designed for repositories with strict commit conventions, pre-commit hooks, and branch protection. | project-management, lifecycle, ci, pr-review, automation | 1.0.0 |
| [global-instructions](contributors/tykeal/instructions/global-instructions) | instructions | copilot | Global Copilot CLI instructions covering commit hygiene (signed, verified commits and a rubber-duck review cycle), PR creation with a mandatory Copilot review loop, and CI/merge expectations. | instructions, global, commit-signing, pr-review | 1.0.0 |

<!-- END INDEX -->

## License

Licensed under the [Apache License 2.0](LICENSES/Apache-2.0.txt) unless an
individual entry declares a different SPDX `license` in its `metadata.yaml`.

[reuse]: https://reuse.software/
