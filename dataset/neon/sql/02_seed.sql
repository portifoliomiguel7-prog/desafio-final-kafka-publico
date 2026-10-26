-- DECISAO DO PROJETO: seed=42, formulas aprovadas; sem random/now/UPSERT.
BEGIN;
SET LOCAL TIME ZONE 'UTC';
LOCK TABLE payments.customers, payments.accounts, payments.cards,
 payments.merchants, payments.transactions IN ACCESS EXCLUSIVE MODE;
DO $$ BEGIN
 IF EXISTS (SELECT 1 FROM payments.customers) OR EXISTS (SELECT 1 FROM payments.accounts)
 OR EXISTS (SELECT 1 FROM payments.cards) OR EXISTS (SELECT 1 FROM payments.merchants)
 OR EXISTS (SELECT 1 FROM payments.transactions) THEN
  RAISE EXCEPTION 'H03_SEED_NONEMPTY: abort; existing data preserved';
 END IF;
END $$;
INSERT INTO payments.customers
 SELECT i, 'Synthetic customer ' || i, 'ACTIVE', timestamptz '2026-01-01 00:00:00+00'
 FROM generate_series(1,200) AS g(i);
INSERT INTO payments.accounts
 SELECT i, 1+((i-1+42)%200), 'ACTIVE', (100000+((i*3571+42)%900000))::numeric/100,
 'BRL', timestamptz '2026-01-02 00:00:00+00', timestamptz '2026-01-02 00:00:00+00'
 FROM generate_series(1,240) AS g(i);
INSERT INTO payments.cards
 SELECT i, 1+((i-1+42)%240), 'synthetic-card-42-' || i, 'ACTIVE',
 timestamptz '2026-01-03 00:00:00+00', timestamptz '2026-01-03 00:00:00+00'
 FROM generate_series(1,320) AS g(i);
INSERT INTO payments.merchants
 SELECT i, 'Synthetic merchant ' || i, (ARRAY['RETAIL','FOOD','SERVICES'])[1+((i-1+42)%3)],
 timestamptz '2026-01-01 00:00:00+00' FROM generate_series(1,60) AS g(i);
INSERT INTO payments.transactions
 SELECT i, c.card_id, c.account_id, 1+((i-1+42)%60),
 (100+((i*7919+42)%999900))::numeric/100, 'BRL', 'APPROVED',
 timestamptz '2026-01-04 00:00:00+00' + i*interval '120 seconds',
 timestamptz '2026-01-04 00:00:00+00' + i*interval '120 seconds',
 timestamptz '2026-01-04 00:00:00+00' + i*interval '120 seconds'
 FROM generate_series(1,2000) AS g(i)
 JOIN payments.cards c ON c.card_id=1+((i-1+42)%320);
DO $$ BEGIN
 IF (SELECT count(*) FROM payments.customers) <> 200
 OR (SELECT count(*) FROM payments.accounts) <> 240
 OR (SELECT count(*) FROM payments.cards) <> 320
 OR (SELECT count(*) FROM payments.merchants) <> 60
 OR (SELECT count(*) FROM payments.transactions) <> 2000 THEN
  RAISE EXCEPTION 'H03_SEED_COUNT_MISMATCH';
 END IF;
END $$;
COMMIT;
