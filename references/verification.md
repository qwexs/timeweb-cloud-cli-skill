# Compatibility and verification

Checked on **2026-10-15** for skill version **1.0**, under the MIT license. This document contains no account inventory or credentials.

## CLI compatibility

- Official GitHub and PyPI stable releases agree on **2.15.4** (2026-09-22). Source is pinned to commit **e4aacf3ed081630ebfa288779a707b91c4a954f8**; see [version evidence](versions.md).
- The installed **2.15.2** baseline and isolated **2.15.4** each passed **207 visible command/group help checks**, with a disposable home, TWC variables removed and socket connections blocked. Their compact command/parameter schemas match. No new command/flag was found in this patch upgrade.
- Recipes/options are checked against [cli-schema.json](cli-schema.json); 34 important flags were also explicitly compared. Source was reviewed for auth precedence, config handling, logging, filtering/output behavior, endpoint changes and the actual singular GPU flag.
- Main skill: **1,834 characters**, approximately **458 tokens** by the skill-creator four-characters/token estimate. Details are loaded progressively. The host's skill-creator validator accepts the frontmatter, including metadata.version and license.

## Offline package checks

Run from the repository root:

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

These checks require Python 3.9+ and no cloud credentials or third-party dependencies.

The validator checks local references, command examples/options, UTF-8 files, symlinks, forbidden account artifacts, credential signatures, personal absolute paths and final MIT licensing. Six regression tests cover package validity, licensing, private paths, synthetic credentials, safe documentation and invalid commands/flags. All checks passed for the release package; Git diff whitespace checks and independent private-marker scans also passed.

ZIP exports use an explicit public-file allowlist under one timeweb-cloud-cli/ root. They exclude Git metadata, caches, virtual environments, backups, credentials and historical local helpers. Entries, content, checksum and archive integrity are checked after creation.

## Limited live verification

A separately user-authorized read-only server-list call succeeded with the existing installed CLI and existing credentials. Version/help and the official HTTPS endpoint were checked first; debug was disabled. Raw stdout/stderr stayed in memory and only allowlisted inventory fields were reported privately. The number of retrieved resources matched the API total, rather than assuming that a 500-item limit implies completeness.

This confirms server listing only, not other APIs or the newer release's endpoint fixes. No account/resource identifiers, resource names, addresses, inventory counts or credentials are included in the public package.

## Limits

No cloud resource creation, paid operations, deletion, DNS/firewall/network changes, auth/config changes or new credential input were part of verification. Apart from the explicitly authorized inventory read, compatibility tests were offline or used public documentation. Secret scanning is heuristic; review proposed changes and use independent scanning where available.
