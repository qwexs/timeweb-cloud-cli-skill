---
name: timeweb-cloud-cli
description: Operate Timeweb Cloud with the official twc CLI. Use for cloud inventory, servers, databases, storage, Kubernetes, apps, DNS and networking.
license: MIT
metadata:
  version: "1.0"
---

# Timeweb Cloud CLI

Use official **twc-cli** (executable **twc**), not the unrelated PyPI package twc.

1. Run `twc --version` and `twc --help`. Read [setup](references/setup.md) for installation, auth and profiles; never install, upgrade or change auth/config without authorization.
2. Read [commands](references/commands.md) for the relevant service. Check each intended command with `--help`; flags and positional arguments differ. [Command index](references/command-index.md) is discovery, not permission to execute.
3. Resolve account/profile and exact resource IDs using scoped reads. Treat names as ambiguous. Never cross accounts or projects without approval.
4. For creation, paid capacity, disruptive changes, credentials, DNS/network/firewall changes, uploads or deletion: explain target, cost/data/availability impact and rollback; obtain explicit approval before executing. Never infer approval from this skill. Do not bypass prompts with force/yes flags unless specifically approved.
5. Read-only is not secret-free: allowlist fields before tool output reaches chat/logs. Never return raw account/server JSON, tokens, passwords, cloud-init, VNC/S3 credentials or kubeconfig. Do not use verbose/debug logging for account operations. See [security](SECURITY.md).
6. Execute only authorized operations, verify with a scoped read, report sanitized results and uncertainty. Do not retry a mutation blindly after timeout.

Verified against **2.15.4** on **2026-10-15**. See [version evidence](references/versions.md); recheck upstream when stale. Offline help checks do not prove live API success.
