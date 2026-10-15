#!/usr/bin/env python3
"""Offline help/schema collector. Requires the pinned official twc-cli environment.
Usage: python scripts/collect_cli_schema.py --output schema.json
No cloud calls, home configuration, credentials or mutation callbacks are used.
"""
import argparse
import contextlib
import datetime
import io
import json
import os
from pathlib import Path
import socket
import tempfile
from importlib.metadata import version


def collect():
    # Only a short-lived process is altered. Never log inherited environment.
    for key in list(os.environ):
        if key.startswith('TWC') or key.lower().endswith('_proxy'):
            os.environ.pop(key)
    with tempfile.TemporaryDirectory(prefix='twc-help-') as home:
        os.environ.update(HOME=home, USERPROFILE=home, NO_COLOR='1', COLUMNS='120')

        def blocked(*args, **kwargs):
            raise RuntimeError('Network forbidden during help validation')

        socket.socket.connect = blocked
        socket.create_connection = blocked
        from twc.__main__ import cli
        from typer.main import get_command
        from click import Context, Group
        from click.testing import CliRunner
        root = get_command(cli)
        schema = {}
        runner = CliRunner()

        def walk(command, parts):
            if command.hidden:
                return
            name = ' '.join(['twc'] + parts)
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                command.get_help(Context(command, info_name=name))
            # Eager --help exits before required arguments and action callbacks.
            result = runner.invoke(root, parts + ['--help'])
            if result.exit_code:
                raise RuntimeError('Help failed for ' + name)
            params = [p for p in command.params if not getattr(p, 'hidden', False)]
            schema[name] = {
                'options': sorted({o for p in params for o in p.opts + getattr(p, 'secondary_opts', []) if o.startswith('-')} | {'--help'}),
                'arguments': [p.name for p in params if not p.opts or not p.opts[0].startswith('-')],
            }
            if isinstance(command, Group):
                for key, child in sorted(command.commands.items()):
                    walk(child, parts + [key])

        walk(root, [])
        return {'cli_version': version('twc-cli'), 'checked_on': datetime.date.today().isoformat(),
                'network': 'blocked', 'authentication': 'none', 'commands': schema}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; choose a fresh path and review before replacing')
    data = collect()
    args.output.write_bytes((json.dumps(data, indent=2) + chr(10)).encode('utf-8'))
    print(json.dumps({'version': data['cli_version'], 'help_checks': len(data['commands']), 'network': 'blocked'}))
