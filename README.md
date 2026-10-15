# Timeweb Cloud CLI skill

A portable, model-agnostic agent skill for the official [Timeweb Cloud CLI](https://github.com/timeweb-cloud/twc). Independent documentation and guardrails, not an official Timeweb product or a replacement CLI.

**Skill version:** 1.0 · **CLI verified:** 2.15.4 · **Checked:** 2026-10-15

## Install the skill

Copy this repository's contents into your agent's skill directory under a folder named `timeweb-cloud-cli`, keeping `SKILL.md`, `references/` and `SECURITY.md` together. For OpenClaw, use your configured workspace's `skills/timeweb-cloud-cli/`. Reload skills as required by the host. Other skill-capable agents can use the same files; no model or shell is assumed.

Installing a skill does **not** install the CLI or authorize cloud changes. Follow [setup](references/setup.md) for isolated CLI installation and private authentication. Never commit credentials.

## Use

Ask your agent:
- “Show a sanitized inventory of servers in this profile; do not change anything.”
- “Propose creating a server in this region, including price assumptions; wait for approval.”
- “Check the exact DNS command and propose the change without applying it.”

Start at [SKILL.md](SKILL.md). Load [recipes](references/commands.md), [command index](references/command-index.md) or [version evidence](references/versions.md) only as needed. Snippets are examples, not scripts to run wholesale.

## Layout and checks

- `SKILL.md` — short workflow.
- `references/` — setup, recipes, generated discovery index, version provenance and compact command schema.
- `scripts/validate.py` — dependency-free offline structural/privacy/example checks; no cloud access.
- `tests/` — validator regression tests.
- `SECURITY.md` and `CONTRIBUTING.md` — safe reporting and maintenance.

From the repository root, with Python 3.9+:

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

Checks do not exercise accounts or prove live API availability. See [verification report](references/verification.md).

## License

[MIT](LICENSE) © 2026 Sergey Pastukhov. Upstream CLI licensing is separate; no CLI source or dependencies are vendored.

Source repository: [qwexs/timeweb-cloud-cli-skill](https://github.com/qwexs/timeweb-cloud-cli-skill).

## По-русски

Навык использует официальный пакет **twc-cli**, команда **twc**. Это инструкции для агента, не облачный клиент. Сначала — версия, справка и безопасное чтение; создание платных ресурсов, удаление и сетевые изменения — только после подтверждения. В пакет не входят токены, конфиги аккаунта и старые локальные помощники. Лицензия — MIT.
