#!/usr/bin/env python3
"""Offline structure, reference, command-example and heuristic privacy checks.
No third-party dependencies, credentials, subprocesses or cloud access.
"""
import json
from pathlib import Path
import re
import shlex
import sys

SKILL_NAME = 'timeweb-cloud-cli'
PATTERNS = {
    'private absolute path': r'(?i)(?:[a-z]:[\\/](?:users|documents and settings)[\\/]|/(?:home|Users)/[a-z0-9_-]+/)',
    'private key': r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----',
    'JWT-like value': r'eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}',
    'provider token': r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})',
    'credential assignment': r'(?i)(?:TWC_TOKEN|root_pass|vnc_pass|secret_access_key)\s*[=:]\s*[\"\']?[A-Za-z0-9_+/=-]{16,}',
}
FORBIDDEN_NAMES = {'.env', '.twcrc', '.twcrc.toml', '.s3cfg', 'kubeconfig', 'account.json', 'server-list.js', 'server-get.js', 'server-logs.js', 'whoami.js'}


def privacy_findings(text):
    return [label for label, pattern in PATTERNS.items() if re.search(pattern, text)]


def command_error(example, schema):
    try:
        words = shlex.split(example)
    except ValueError:
        return 'unbalanced command quoting'
    if not words or words[0] != 'twc':
        return None
    # Root options each consume a value; help/version have no value.
    at = 1
    while at < len(words) and words[at] in ('--profile', '-p', '--config', '-c'):
        at += 2
    tail = words[at:]
    candidates = [(key, key.split()[1:]) for key in schema]
    candidates = [(key, parts) for key, parts in candidates if tail[:len(parts)] == parts]
    key, parts = max(candidates, key=lambda item: len(item[1]))
    remaining = tail[len(parts):]
    # Bare unknown words after root/group are likely invented commands.
    children = any(k.startswith(key + ' ') for k in schema)
    if remaining and not remaining[0].startswith('-') and children:
        return 'unknown command after ' + key
    for word in remaining:
        if word.startswith('-') and word.split('=')[0] not in schema[key]['options']:
            return 'unknown option ' + word + ' for ' + key
    return None


def validate(root):
    issues = []
    skill = (root / 'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n') or 'name: ' + SKILL_NAME not in skill:
        issues.append('invalid skill frontmatter/name')
    if len(skill) // 4 >= 500:
        issues.append('SKILL.md exceeds approximate 500-token budget')
    if 'metadata:\n  version:' not in skill:
        issues.append('missing skill version metadata')
    if re.search(r'(?i)sonnet|gpt-?5|opus|haiku|minimax', skill):
        issues.append('model-specific main skill')
    license_path = root / 'LICENSE'
    if not license_path.is_file() or not license_path.read_text(encoding='utf-8').startswith('MIT License\n'):
        issues.append('missing or invalid MIT LICENSE')
    if (root / 'LICENSE-MIT.proposed').exists():
        issues.append('obsolete proposed license in release tree')
    if 'license: MIT' not in skill:
        issues.append('missing MIT license metadata')
    schema_data = json.loads((root / 'references/cli-schema.json').read_text(encoding='utf-8'))
    schema = schema_data['commands']
    count = 0
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if any(part in ('.git', '__pycache__') for part in relative.parts):
            continue
        if path.is_symlink():
            issues.append(str(relative) + ': symlink forbidden')
        if not path.is_file():
            continue
        count += 1
        if path.name in FORBIDDEN_NAMES or path.suffix in ('.pem', '.key', '.pfx', '.zip', '.pyc'):
            issues.append(str(relative) + ': private/generated artifact forbidden')
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            issues.append(str(relative) + ': unexpected binary/non-UTF8 file')
            continue
        for finding in privacy_findings(text):
            issues.append(str(relative) + ': ' + finding)
        if path.suffix != '.md':
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if re.match(r'https?://|mailto:|#', target):
                continue
            resolved = (path.parent / target.split('#')[0]).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                issues.append(str(relative) + ': missing/escaping reference ' + target)
        examples = []
        # Inline code and plain command lines in code fences.
        examples.extend(re.findall(chr(96) + r'(twc(?:\s+[^' + chr(96) + r'\n]*)?)' + chr(96), text))
        examples.extend(line.strip() for line in text.splitlines() if line.strip().startswith('twc '))
        for example in examples:
            error = command_error(example, schema)
            if error:
                issues.append(str(relative) + ': ' + error)
    return {'ok': not issues, 'files': count, 'cli_version': schema_data['cli_version'], 'command_paths': len(schema), 'issues': issues}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = validate(root)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result['ok'] else 1)
