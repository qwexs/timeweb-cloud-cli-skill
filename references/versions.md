# Version evidence (checked 2026-10-15)

## Official sources

- [Timeweb documentation landing page](https://timeweb.cloud/docs/twc-cli) links the official repository, PyPI distribution and guide.
- [Repository](https://github.com/timeweb-cloud/twc), [latest release endpoint](https://api.github.com/repos/timeweb-cloud/twc/releases/latest), [PyPI metadata](https://pypi.org/pypi/twc-cli/json).
- Latest stable on both registries: **2.15.4**. GitHub published **2026-09-22T15:35:33Z**; PyPI wheel uploaded **2026-09-22T15:35:46Z** (rounded to seconds). Python requirement: **>=3.8.19,<4.0.0**.
- [Release v2.15.4](https://github.com/timeweb-cloud/twc/releases/tag/v2.15.4), pinned commit **e4aacf3ed081630ebfa288779a707b91c4a954f8**.
- [Pinned changelog](https://github.com/timeweb-cloud/twc/blob/v2.15.4/CHANGELOG.md), [guide](https://github.com/timeweb-cloud/twc/blob/v2.15.4/docs/ru/README.md), [CLI reference](https://github.com/timeweb-cloud/twc/blob/v2.15.4/docs/ru/CLI_REFERENCE.md).

## Installed baseline vs latest

Research workstation had **2.15.2**, verified with version/help. A disposable environment with **2.15.4** was installed solely for offline help/schema checking; the global installation was not updated. Both expose **207 visible command/group paths** with identical parameter schemas. There are **no new commands or flags between 2.15.2 and 2.15.4**; changes are API compatibility fixes:

| Release | Change |
| --- | --- |
| 2.15.3 (2026-09-14) | Database preset listing uses the newer API endpoint. |
| 2.15.4 (2026-09-22) | Kubernetes network-driver listing uses the newer API endpoint; fixes adding subdomain DNS A records. |

These are upstream release/source claims, not live account tests. Relevant source: [API client](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/api/client.py) and [DNS commands](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/commands/domain.py).

## Capabilities absent from the old short skill, not necessarily new to the installed CLI

- 2.15.0: server hostname via --hostname.
- 2.14.0: server list-configurators; 2.14.1 fixes cloud-init user-data file handling.
- 2.13.0: Cloud Apps service (apps).
- 2.12.0: balancer timeout/max-connections settings; default S3 endpoint changed to s3.twcstorage.ru. Discover service-specific endpoints rather than hardcoding a universal one.
- 2.11.0: balancer presets, private/public networking and TLS options.
- 2.10.0: database types, users, instances, backup schedules and network options; --network-id replaces deprecated --network for servers.
- 2.9.0: GPU/Dedicated CPU provisioning. **Changelog mentions --gpus, but actual 2.15.4 help/source use --gpu (singular)**. Follow help/source, not that historical spelling.
- 2.8.0: DNS SRV records and TTL; 2.7.0: whoami; 2.6.0: firewall dump/restore and IPv6 rules; 2.5.0: top-level ip replaces deprecated server ip.

## Other correctness/security evidence

[Auth wrapper](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/apiwrap.py) resolves TWC_TOKEN before config token. [Common options](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/commands/common.py) define profiles/config/output. [Configuration commands](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/commands/config.py) show unmasked input/plaintext storage. [API base](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/api/base.py) redacts auth headers but logs response bodies. The guide states --filter only affects default output. [Storage help/source](https://github.com/timeweb-cloud/twc/blob/v2.15.4/twc/commands/storage.py) explicitly excludes S3 object operations.

## Refresh procedure

Check official latest endpoints again; distinguish stable releases from prereleases/yanked packages. Install a pinned release in a disposable environment. Run scripts/collect_cli_schema.py there with an explicit output path, compare schemas, review source/changelog, regenerate the index and update recipes. Run offline validation and skill-creator validation. Never authenticate or test writes merely to refresh documentation. See CONTRIBUTING.md.
