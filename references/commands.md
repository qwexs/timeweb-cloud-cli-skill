# Command recipes (2.15.4)

Use canonical names. [Generated index](command-index.md) covers the wider surface; exact help wins. Uppercase identifiers are placeholders. Reads require an authorized account/scope and private output handling.

## Inventory and catalogs

```text
twc whoami
twc account status --output json
twc server list --output json --limit 500
twc server get SERVER_ID --output json
twc server list-presets
twc server list-configurators
twc server list-os-images
twc server list-software
twc database list --output json
twc database list-types
twc database list-presets
twc storage list --output json
twc cluster list --output json
twc cluster list-k8s-versions
twc cluster list-network-drivers
twc image list
twc ip list
twc balancer list
twc balancer list-presets
twc apps list
twc apps list-presets
twc apps get-vcs-providers
twc domain list
twc domain record list example.org --all
twc vpc list
twc firewall group list
twc project list
twc ssh-key list
```

Check limits and command-specific pagination: 500 results are not proof of complete inventory. There is no universal pagination flag. Kubernetes details use `twc cluster show CLUSTER_ID`, not a guessed get command.

## Output is NOT sanitization

`--output/-o` supports default, raw, json, yaml where exposed; it is not a universal root option. Capture JSON privately and **allowlist before agent tool/chat/log output**. Server responses can include root/VNC passwords and cloud-init; account responses contain personal/billing data. Expose only needed ID/name/status/location/capacity fields; names and IP addresses can also be sensitive.

For human tables only:

```text
twc server list --filter status:on,location:ru-1
```

`--filter/-f` affects default presentation, **not JSON/YAML/raw**, and is not server-side access control. Filter JSON in a private pipeline and project approved fields. Do not send raw responses to the agent merely to redact afterward.

## Propose changes, then stop for approval

Only inspect help until target, price/region, account/project, consequences and rollback are confirmed:

```text
twc server create --help
twc server resize --help
twc server reinstall --help
twc server remove --help
twc database create --help
twc database user create --help
twc database instance create --help
twc database backup schedule --help
twc apps create --help
twc domain record add --help
twc firewall group restore --help
twc ip create --help
```

Server create requires `--name`, `--image` and an appropriate sizing choice: `--preset-id` OR explicit capacity. Verified options include `--configurator-id`, `--type`, **`--gpu` (singular)**, `--hostname`, `--user-data`, `--network-id`, `--public-ip` / `--no-public-ip`, `--private-ip`, `--region`, `--availability-zone`, `--project-id`, `--ssh-key`, `--disable-ssh-password-auth`. GPU implies premium; preset and CPU/RAM/disk/GPU sizing are mutually exclusive. Discover live catalogs; don't reuse stale price/preset IDs. Cloud-init files can carry secrets and must not enter repositories.

Cloud Apps creation takes positional `YML_CONFIG_PATH`. Inspect [source](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/commands/apps.py) before preparing private YAML. `--status` reports deployment status; it does not make creation read-only.

DNS add takes `DOMAIN_NAME`; options include `--type`, `--value`, `--ttl`, `--prio`; SRV uses `--service`, `--proto`, `--host`, `--port`. Update has different flags: do not copy add syntax blindly.

Load balancer create/set supports timeout/max-connections settings. Prefer `--network-id` over hidden deprecated `--network`. Database create uses `--user-login` / `--user-password`, not old `--login` / `--password`. Avoid password arguments in history/process listings; use a supported private mechanism or stop for a safer workflow.

## Boundaries and credential-producing commands

- `storage` is bucket control-plane management, **not object upload/download**. Use a separately approved S3 client for objects. Bucket visibility/retention and `storage rb` can disclose/destroy data.
- `storage genconfig` creates S3-client credentials; `cluster kubeconfig` emits cluster credentials; `server vnc` exposes console access. These require sensitive delivery, not ordinary inventory.
- Floating IPs use top-level `ip`; `server ip` is deprecated. IP allocation and GPU/capacity creation incur costs.
- Firewall restore/link/unlink, DNS and network changes can lock out access: inspect and preserve existing state first.
- After approved mutation, perform a narrow read. Reconcile after timeout before retry: creation may already have succeeded.
