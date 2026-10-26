"""Standalone public package audit: manifest, privacy, evidence and offline integrity.

Independent package-specific policy, not a copy of the previous Git-history rules.
No network, Git, SDK or external process is invoked.
"""
import argparse
from collections import Counter
from decimal import Decimal
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import sys


def check(root, strict=False):
    manifest = json.loads((root / 'release-manifest.json').read_text(encoding='utf-8'))
    expected = set(manifest['files']) | {'release-manifest.json'}
    known_paths = list(expected) + [source['private_path'] for item in manifest['files'].values()
                                   for source in item['private_sources']]
    actual = set()
    for path in root.rglob('*'):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError('Symlink rejected: ' + relative)
        private = (relative in {'.env', '.local', '.git'} or relative.startswith(('.local/', '.git/')))
        if private and not strict:
            continue
        if path.is_file():
            actual.add(relative)
        if strict and any(part in {'.git', '.env', '.local', '.course-context', '__pycache__'} for part in path.relative_to(root).parts):
            raise ValueError('Export contains private/runtime artifact: ' + relative)
    if actual != expected:
        raise ValueError('Allowlist mismatch: ' + ', '.join(sorted(actual ^ expected)))
    links = 0
    jsons = 0
    for name in sorted(expected):
        path = root / name
        raw = path.read_bytes()
        if name != 'release-manifest.json':
            if hashlib.sha256(raw).hexdigest() != manifest['files'][name]['export_sha256']:
                raise ValueError('Manifest hash mismatch: ' + name)
        text = raw.decode('utf-8')
        # Independent privacy/credential surface rules, never echo the match.
        rules = [r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b',
                 r'[A-Za-z]:[\\/]Users[\\/]', r'/(?:Users|home)/[^\s/]+/',
                 r'\b(?:sa|u|env|lkc|lcc|lsrc|lfcp|rb)-[A-Za-z0-9]{4,}\b',
                 r'(?:ep-|pkc-|psrc-)[\w.-]+\.(?:neon\.tech|confluent\.cloud)',
                 r'postgres(?:ql)?://[^\s:/]+:[^\s@]+@',
                 r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----',
                 r'\b(?:AKIA[A-Z0-9]{16}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})\b']
        if any(re.search(rule, text) for rule in rules):
            raise ValueError('Privacy/secret policy requires review: ' + name)
        for token in re.findall(r'[A-Za-z0-9+/=_-]{40,}', text):
            if any(token in path for path in known_paths):
                continue  # Relative paths identified in the allowlist/provenance are not secrets.
            counts = Counter(token)
            entropy = -sum((v / len(token)) * math.log2(v / len(token)) for v in counts.values())
            if entropy >= 4.5:
                raise ValueError('High-entropy token requires review: ' + name)
        if re.search(r'"raw_(?:key|value)_base64"', text):
            raise ValueError('Raw wire payload must be excluded: ' + name)
        if name.endswith('.json'):
            parsed = json.loads(text); jsons += 1
            def credential_fields(value):
                if isinstance(value, dict):
                    for key, item in value.items():
                        if re.search(r'(?:password|api[_-]?key|api[_-]?secret|access[_-]?token)$', key, re.I):
                            if isinstance(item, str) and item and not item.startswith(('${', '<', '[REDACTED')):
                                raise ValueError('Credential field requires review: ' + name)
                        credential_fields(item)
                elif isinstance(value, list):
                    for item in value:
                        credential_fields(item)
            credential_fields(parsed)
        if name.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if re.match(r'[a-z]+://', target):
                    continue
                target = target.split('#')[0]
                if target:
                    resolved = (path.parent / target).resolve()
                    if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                        raise ValueError('Broken/escaping link: ' + name)
                    links += 1
    load = lambda name: json.loads((root / name).read_text(encoding='utf-8'))['data']
    foundation = load('evidencias/H01/access-tests.json')
    assert len(foundation['tests']) == 4 and all(item['status'] == 'PASS' for item in foundation['tests'])
    avro = load('evidencias/H02/avro-compatibility.json')
    steps = {step['name']: step for step in avro['steps']}
    assert steps['register_v1']['http_status'] == steps['register_v2']['http_status'] == 200
    assert steps['register_v3_rejected']['http_status'] == 409
    database = load('evidencias/H03/database.json')
    assert [database['dataset'][table]['count'] for table in ['customers', 'accounts', 'cards', 'merchants', 'transactions']] == [200, 240, 320, 60, 2000]
    enrichment = load('evidencias/H06/enrichment.json')
    assert enrichment['logical_current_rows'] == 2000 and enrichment['all_nine_fields'] == 'PASS'
    assert enrichment['current_committed_state'] == 'NOT_PROVEN'
    cdc = load('evidencias/01-envelopes-cdc.json')
    events = {item['action_id']: item['event'] for item in cdc['events']}
    assert len(events) == 4
    for action, op in [('INSERT_TRANSACTION', 'c'), ('UPDATE_ACCOUNT', 'u'), ('DELETE_TRANSACTION', 'd')]:
        assert events[action]['value']['op'] == op
    creation, update, deletion = [events[name]['value'] for name in ['INSERT_TRANSACTION', 'UPDATE_ACCOUNT', 'DELETE_TRANSACTION']]
    assert creation['before'] is None and creation['after'] is not None
    assert update['before'] != update['after'] and update['before'] is not None and update['after'] is not None
    assert deletion['after'] is None and deletion['before'] is not None
    tomb, deleted = events['DELETE_TOMBSTONE'], events['DELETE_TRANSACTION']
    assert tomb['value'] is None and tomb['offset'] == deleted['offset'] + 1
    assert all(tomb[k] == deleted[k] for k in ['key', 'topic', 'partition'])
    p1 = load('evidencias/H07/P1.json')
    alert = {**p1['alert']['key'], **p1['alert']['value']}
    inputs = {row['transaction_id']: row for row in p1['insert_rows']}
    creations = {event['key']['transaction_id']: event['value'] for event in p1['creation_events']}
    instant = lambda value: dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    ids = [alert[f'tx{n}_id'] for n in (1, 2, 3)]
    assert ids == [102001, 102002, 102003] and alert['card_id'] == 1 and alert['txn_count'] == 3
    for n, pk in enumerate(ids, 1):
        row, event = inputs[pk], creations[pk]
        assert row['card_id'] == event['card_id'] == alert['card_id']
        assert Decimal(row['amount']) == Decimal(event['amount']) == Decimal(alert[f'tx{n}_amount'])
        assert row['status'] == event['transaction_status'] == alert[f'tx{n}_status']
        assert instant(row['occurred_at']) == instant(event['event_time']) == instant(alert[f'tx{n}_time'])
    first, last = instant(alert['first_event_time']), instant(alert['last_event_time'])
    assert (last - first) // dt.timedelta(milliseconds=1) == alert['interval_ms'] == 40000
    fmt = lambda t: t.strftime('%Y-%m-%d %H:%M:%S.') + f'{t.microsecond // 1000:03d}'
    canonical = 'RULE_VELOCITY-v1|CREATION_EVENT|1|102001,102002,102003|' + fmt(first) + '|' + fmt(last)
    assert hashlib.sha256(canonical.encode()).hexdigest() == alert['alert_id']
    assert p1['verification']['observed_after_interruption'] and not p1['verification']['planned_advancer_submitted']
    n1, n2, b1 = [load('evidencias/H07/' + n + '.json') for n in ['N1', 'N2', 'B1']]
    assert n1['status'] == 'PASS' and n1['new_alerts'] == 0
    assert n2['status'] == 'PASS_RETROSPECTIVE' and n2['new_alerts'] == 0
    assert len({row['card_id'] for row in n2['rows'][:3]}) == 3
    assert b1['expected_interval_ms'] == 59999 and b1['observed_interval_ms'] == 59000 and b1['status'] == 'FAIL_INTERVAL_MS'
    assert hashlib.sha256(b1['canonical'].encode()).hexdigest() == b1['alert_id']
    parts = b1['canonical'].split('|')
    assert (instant(parts[-1]) - instant(parts[-2])) // dt.timedelta(milliseconds=1) == 59999
    assert b1['SHA256'] == b1['witnesses'] == 'PASS'
    assert n1['current_read_reached_high'] and n2['current_read_reached_high']
    assert n1['elapsed_since_last_creation_ms'] >= 35000 and n2['elapsed_since_last_creation_ms'] >= 35000
    billing = load('evidencias/H08/billing.json')
    rows = billing['capture']['response']
    amount = lambda value: Decimal(str(value).replace('$', '').replace(',', '').strip())
    usage = sum((amount(row['amount']) for row in rows if row['line_type'] != 'PROMO_CREDIT'), Decimal(0))
    credit = sum((amount(row['amount']) for row in rows if row['line_type'] == 'PROMO_CREDIT'), Decimal(0))
    assert len(rows) == 60 and usage == Decimal('254.0597') and credit == Decimal('-254.0599')
    assert usage + credit == Decimal('-0.0002')
    obs = load('evidencias/H08/observability.json')
    assert obs['query_count'] == 0 and obs['received_bytes']['peak'] is None and obs['consumer_lag']['value'] is None
    assert manifest['publication'] in {'NOT_AUTHORIZED', 'AUTHORIZED_SANITIZED_EXPORT'}
    assert manifest['H09'] == 'PARTIAL — PUBLIC_RELEASE_CANDIDATE_PREPARED'
    if manifest['publication'] == 'AUTHORIZED_SANITIZED_EXPORT':
        if not isinstance(manifest.get('public_repository'), str) or not re.fullmatch(r'[A-Za-z0-9-]+/[a-z0-9][a-z0-9-]*', manifest['public_repository']):
            raise ValueError('Authorized export lacks a valid explicit public destination')
        if 'https://github.com/' + manifest['public_repository'] not in (root / 'README.md').read_text(encoding='utf-8'):
            raise ValueError('Public destination differs between README and manifest')
    return {'status': 'PASS_PUBLIC_CANDIDATE_LOCAL_CHECK', 'files': len(expected), 'JSONs': jsons,
            'links': links, 'privacy_policy': 'PASS', 'CDC_P1_B1_Billing': 'PASS', 'cloud_calls': 0,
            'limits': 'Selection only; no wire replay, cloud reconstruction or universal secret/PII certification'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-export', action='store_true')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.root.resolve(), args.strict_export), ensure_ascii=False))
        return 0
    except (ValueError, OSError, AssertionError) as exc:
        print('BLOCKED: ' + (str(exc) if str(exc) else 'Evidence consistency assertion failed'), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
