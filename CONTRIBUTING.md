# Contributing

Keep the skill short, portable and model-agnostic. Detail belongs in references, not personal paths or provider/model defaults. Do not add API wrappers or bundled cloud credentials.

1. Compare official GitHub and PyPI stable releases; pin evidence to a tag/commit.
2. Use a disposable CLI environment. No global upgrade, authentication/config change or live API call is needed for documentation work.
3. Inspect source and run version/help only with disposable home, cleared TWC variables and network blocked. Never test mutations.
4. Update version evidence and compact schema when CLI changes. Verify paths, actual flags, arguments, deprecations and filter/output semantics.
5. Run `python scripts/validate.py` and `python -m unittest discover -s tests -v`. Run the host's skill-creator validator too when available.
6. Review staged files for secrets/paths/account artifacts. Rebuild archives from an allowlist, excluding Git metadata, environments, backups and caches.

No real account fixtures, environment dumps, raw responses or private aliases. Distinguish offline checks from unperformed live API tests. Contributions to this package are submitted under its MIT license. Keep upstream attribution and licensing separate when adding third-party material.
