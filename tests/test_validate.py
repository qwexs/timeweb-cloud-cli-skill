import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class ValidationTests(unittest.TestCase):
    def test_package(self):
        self.assertEqual(v.validate(ROOT)['issues'], [])

    def test_release_license(self):
        text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('MIT License\n'))
        self.assertNotIn('PROPOSAL ONLY', text)
        self.assertFalse((ROOT / 'LICENSE-MIT.proposed').exists())

    def test_private_paths(self):
        self.assertIn('private absolute path', v.privacy_findings('C:' + '/' + 'Users/' + 'Example' + '/file'))
        self.assertIn('private absolute path', v.privacy_findings('/' + 'home/' + 'example' + '/file'))

    def test_synthetic_secrets(self):
        self.assertIn('private key', v.privacy_findings('-----BEGIN ' + 'PRIVATE KEY-----'))
        self.assertIn('credential assignment', v.privacy_findings('TWC_TOKEN' + '=' + 'a' * 24))
        self.assertIn('provider token', v.privacy_findings('ghp' + '_' + 'a' * 36))

    def test_safe_documentation(self):
        self.assertEqual(v.privacy_findings('TWC_TOKEN overrides config; ~/.twcrc is private.'), [])

    def test_command_and_flags(self):
        schema = {'twc': {'options': ['--help']}, 'twc server': {'options': ['--help']},
                  'twc server create': {'options': ['--help', '--gpu']}}
        self.assertIsNone(v.command_error('twc server create --gpu 1', schema))
        self.assertIsNotNone(v.command_error('twc server create --gpus 1', schema))
        self.assertIsNotNone(v.command_error('twc server invented --help', schema))
        self.assertIsNone(v.command_error('twc --profile PROFILE server create --help', schema))


if __name__ == '__main__':
    unittest.main()
