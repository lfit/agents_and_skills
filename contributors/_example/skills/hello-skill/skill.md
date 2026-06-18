<!--
SPDX-License-Identifier: Apache-2.0
SPDX-FileCopyrightText: 2025 The Linux Foundation
-->

# hello-skill — definition

## When to use

Apply this skill when someone asks how to add a new agent or skill to the
`agents_and_skills` repository.

## Procedure

1. Copy the relevant folder from `templates/` (`agent/` or `skill/`).
2. Place it under `contributors/<your-handle>/<agents|skills>/<name>/`.
3. Fill in `metadata.yaml` (name, description, author, tool, kind, tags,
   version, license).
4. Write the entry `README.md` and the definition file.
5. Sign your commits with GPG and include a DCO `Signed-off-by` line.
6. Open a pull request.

## Notes

- The catalog index in the top-level `README.md` is generated automatically
  from each `metadata.yaml`.
