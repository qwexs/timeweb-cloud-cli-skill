# Security

Never publish credentials/account data in issues, pull requests, examples, screenshots or build logs. Tests do not need a Timeweb account.

Use least-privilege, short-lived credentials where available. Keep API tokens, plaintext CLI config, SSH keys, S3 config, kubeconfig and cloud-init outside this repository. Upstream configuration does not reliably hide input: authenticate in a private local terminal. Never request tokens publicly.

GET/list responses can contain passwords, cloud-init, keys, personal and billing data. Allowlist fields before tool/chat/log output. Avoid verbose/debug logging: header redaction does not sanitize response bodies. Review IP addresses and names too.

Creation, resizing, backups and IP allocation can cost money; deletion/reinstallation can lose data; DNS/firewall/network changes can expose services or remove access. Require exact targets and explicit impact-aware authorization. This package grants no such authorization.

If a credential is exposed, revoke/rotate it first. File removal or Git history rewriting is insufficient. Do not repost it in reports. Use GitHub private vulnerability reporting if enabled by the maintainer. Otherwise share only a credential-free summary and arrange a private channel before sending sensitive details. Never attach account artifacts or working credentials.

The scanner is heuristic, not a complete secret detector. Review staged diffs and run an independent maintained scanner such as Gitleaks before publication when available.
