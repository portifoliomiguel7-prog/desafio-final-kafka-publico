"""Validate sources or prepare local placeholders. No SDK, network or cloud calls."""
import argparse
import json
from pathlib import Path
import sys

REQUIRED = ['.env.example', '.gitignore', 'connectors/cdc.json',
            'schemas/pedido-v1.avsc', 'schemas/pedido-v2.avsc', 'schemas/pedido-v3-quebra.avsc',
            'dataset/neon/sql/01_ddl.sql', 'dataset/neon/sql/02_seed.sql',
            'dataset/neon/sql/03_cdc_setup.sql', 'sql/08-enrichment.sql',
            'sql/09b-fraud-events-bridge.sql', 'sql/10b-fraud-match.sql',
            'docs/08-reproducao-entrega.md', 'docs/09-indice-evidencias.md']


def validate(root):
    for name in REQUIRED:
        p = root / name
        if p.is_symlink() or not p.is_file() or not p.stat().st_size:
            raise ValueError('Required source missing, empty or symlink: ' + name)
    for name in REQUIRED:
        if name.endswith(('.json', '.avsc')):
            json.loads((root / name).read_text(encoding='utf-8-sig'))
    fields = []
    for line in (root / '.env.example').read_text(encoding='utf-8-sig').splitlines():
        if line and not line.startswith('#'):
            key, value = line.split('=', 1)
            if value and (key not in {'POSTGRES_DATABASE', 'CDC_USER'}):
                raise ValueError('Non-placeholder environment template field: ' + key)
            fields.append(key)
    if len(fields) != len(set(fields)):
        raise ValueError('Duplicate template field')
    rules = (root / '.gitignore').read_text(encoding='utf-8')
    if not all(rule in rules.splitlines() for rule in ['.env', '.local/', '.course-context/']):
        raise ValueError('Local ignore guards missing')
    return fields


def prepare(root):
    # Refuse redirects of local writes, including existing symlinks.
    for name in ['.env', '.local', '.local/delivery', '.local/delivery/preparation.json']:
        if (root / name).is_symlink():
            raise ValueError('Local target symlink rejected: ' + name)
    destination = root / '.env'
    created = False
    try:
        with destination.open('xb') as handle:
            handle.write((root / '.env.example').read_bytes())
        created = True
    except FileExistsError:
        if not destination.is_file():
            raise ValueError('Existing .env is not a regular file')
    folder = root / '.local/delivery'
    folder.mkdir(parents=True, exist_ok=True)
    result = {'mode': 'LOCAL_PREPARATION_ONLY', 'environment_created': created,
              'existing_environment_preserved': not created, 'dependencies_installed': False,
              'cloud_calls': 0, 'runtime_ready': False}
    (folder / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true', help='Read-only local validation (default)')
    modes.add_argument('--prepare', action='store_true', help='Create ignored local placeholders, never cloud')
    args = parser.parse_args(argv)
    if sys.version_info < (3, 10):
        parser.error('Python 3.10+ required')
    root = Path(__file__).resolve().parents[2]
    try:
        fields = validate(root)
        result = prepare(root) if args.prepare else {'mode': 'LOCAL_READONLY_CHECK', 'cloud_calls': 0}
        result.update(status='PASS', source_files=len(REQUIRED), environment_template_fields=len(fields))
    except (OSError, ValueError) as exc:
        print('Local preparation FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
