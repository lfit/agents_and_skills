<!--
SPDX-License-Identifier: MIT
SPDX-FileCopyrightText: 2025 Andrew Grimberg <agrimberg@linuxfoundation.org>
-->

# global-instructions

## Overview

`global-instructions` is a set of personal, global GitHub Copilot CLI
instructions. They direct the assistant on commit hygiene (signed and verified
commits, a rubber-duck review cycle), pull request creation with a mandatory
Copilot review loop, and CI/merge expectations.

## Target tool

GitHub Copilot CLI. The instructions apply globally rather than to a single
repository.

## Usage

Copy the definition into your global Copilot configuration:

```shell
cp copilot-instructions.md ~/.copilot/copilot-instructions.md
```

The instructions then apply to every Copilot CLI session for your user.

## Configuration

None. Review the contents and adjust them to match your own workflow before
adopting them.

## Maintainer

- Author: `tykeal`
- Questions or issues: open an issue and mention the author.
