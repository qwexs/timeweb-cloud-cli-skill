# Installation, authentication and profiles

Verified for twc-cli 2.15.4. Official [guide](https://github.com/timeweb-cloud/twc/blob/v2.15.4/docs/ru/README.md) and [PyPI metadata](https://pypi.org/pypi/twc-cli/2.15.4/json).

## Identify before installing

```text
twc --version
twc --help
```

Distribution: **twc-cli**, not **twc** (unrelated TaskWarrior frontend). PyPI declares Python >=3.8.19,<4; prefer maintained Python. This repository's validator needs Python 3.9+.

If installation is requested, choose ONE isolated method:

```text
pipx install twc-cli==2.15.4
```

Or create an environment with `python -m venv .venv`, then use its executable:

```text
# POSIX
.venv/bin/python -m pip install twc-cli==2.15.4
.venv/bin/twc --help
# PowerShell / Windows
.venv/Scripts/python.exe -m pip install twc-cli==2.15.4
.venv/Scripts/twc.exe --help
```

Do not execute both platform variants. No global update is required. On Windows resolve the real executable (e.g. `Get-Command twc`); do not assume a Python version/path. GitHub also ships zipapp artifacts; use official releases instead of an unreviewed download-and-run script.

## Authentication — private local terminal only

If explicitly requested, the user can run `twc config` or `twc config init` in a **private local terminal**. Upstream does not reliably mask input: first-time setup uses plain `input()`, existing profiles use `typer.prompt` without hidden input. Never request tokens in public chat, record the session, or put tokens in command arguments.

Plaintext TOML config: `~/.twcrc` (also recognizes `~/.twcrc.toml`). Protect permissions/ACLs. Never dump it. `TWC_TOKEN` overrides the profile token; provision it privately with the host's secret mechanism. Never print environment values. Other fields can still be read from config: a token alone does not guarantee configuration-free execution.

Root options precede the subcommand:

```text
twc --profile PROFILE whoami
twc --config CONFIG_FILE --profile PROFILE server list --output json
```

Replace placeholders. Selecting an existing profile does not require edits. `whoami` is an API request and reveals login: verify privately and minimize reporting. Confirm account/project before changes. `TWC_PROFILE` and `TWC_CONFIG_FILE` also select them. Privately check unexpected `TWC_ENDPOINT` before sending credentials; never silently redirect to an untrusted endpoint.

`twc config dump`, especially `--full`, can disclose tokens. Avoid it. `--verbose` / `TWC_DEBUG` can expose API response bodies and cloud-init; header token redaction does not protect those bodies. Do not enable logs merely to troubleshoot authentication. Use status codes and sanitized summaries.

Completion installation changes shell configuration: only on request, after inspecting existing setup. `twc --show-completion` allows review without installation.
