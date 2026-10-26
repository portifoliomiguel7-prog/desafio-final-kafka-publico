"""Local preparation guardrails: no network, no overwrite, no escaped writes."""
import importlib.util
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('h09_prepare', ROOT / 'harness/checks/h09-prepare.py')
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='h09-test-', dir=ROOT / '.local')
        self.root = Path(self.temp.name).resolve()
        assert self.root.is_relative_to((ROOT / '.local').resolve())
        for name in prep.REQUIRED:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('{}' if name.endswith(('.json', '.avsc')) else 'source', encoding='utf-8')
        (self.root / '.env.example').write_text('CDC_PASSWORD=\nCDC_USER=cdc_user\n', encoding='utf-8')
        (self.root / '.gitignore').write_text('.env\n.local/\n.course-context/\n', encoding='utf-8')

    def tearDown(self):
        assert self.root.is_relative_to((ROOT / '.local').resolve())
        self.temp.cleanup()

    def test_check_is_read_only(self):
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*'))
        prep.validate(self.root)
        self.assertEqual(before, sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*')))
        self.assertFalse((self.root / '.env').exists())

    def test_existing_environment_preserved_on_repeat(self):
        prep.validate(self.root)
        self.assertTrue(prep.prepare(self.root)['environment_created'])
        marker = b'LOCAL_SENTINEL_NOT_A_CREDENTIAL\n'
        (self.root / '.env').write_bytes(marker)
        self.assertTrue(prep.prepare(self.root)['existing_environment_preserved'])
        self.assertEqual((self.root / '.env').read_bytes(), marker)

    def test_invalid_source_prevents_preparation(self):
        (self.root / 'connectors/cdc.json').write_text('{bad', encoding='utf-8')
        with self.assertRaises(ValueError):
            prep.validate(self.root)
        self.assertFalse((self.root / '.env').exists())

    def test_symlink_redirect_refused_without_write(self):
        with patch.object(Path, 'is_symlink', lambda p: p == self.root / '.local'):
            with self.assertRaises(ValueError):
                prep.prepare(self.root)
        self.assertFalse((self.root / '.env').exists())

    def test_no_socket_or_dns_calls(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('NETWORK_FORBIDDEN')) as conn, \
             patch.object(socket, 'getaddrinfo', side_effect=AssertionError('DNS_FORBIDDEN')) as dns:
            prep.validate(self.root)
            prep.prepare(self.root)
            self.assertFalse(conn.called)
            self.assertFalse(dns.called)


if __name__ == '__main__':
    unittest.main()
