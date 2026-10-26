-- DECISAO DO PROJETO: modelo proprio aprovado para H03. Dados sinteticos.
-- Executar em banco novo; objetos existentes provocam erro, sem sobrescrita.
BEGIN;
CREATE SCHEMA payments;
CREATE TABLE payments.customers (
 customer_id bigint PRIMARY KEY CHECK (customer_id > 0),
 display_name text NOT NULL,
 status text NOT NULL CHECK (status IN ('ACTIVE','INACTIVE')),
 created_at timestamptz NOT NULL
);
CREATE TABLE payments.accounts (
 account_id bigint PRIMARY KEY CHECK (account_id > 0),
 customer_id bigint NOT NULL REFERENCES payments.customers(customer_id),
 status text NOT NULL CONSTRAINT accounts_status_check CHECK (status IN ('ACTIVE','SUSPENDED')),
 balance numeric(15,2) NOT NULL CHECK (balance >= 0),
 currency char(3) NOT NULL CHECK (currency = 'BRL'),
 created_at timestamptz NOT NULL,
 updated_at timestamptz NOT NULL CHECK (updated_at >= created_at)
);
CREATE TABLE payments.cards (
 card_id bigint PRIMARY KEY CHECK (card_id > 0),
 account_id bigint NOT NULL REFERENCES payments.accounts(account_id),
 card_token text NOT NULL UNIQUE,
 status text NOT NULL CHECK (status IN ('ACTIVE','BLOCKED','EXPIRED')),
 created_at timestamptz NOT NULL,
 updated_at timestamptz NOT NULL CHECK (updated_at >= created_at),
 UNIQUE (card_id, account_id)
);
CREATE TABLE payments.merchants (
 merchant_id bigint PRIMARY KEY CHECK (merchant_id > 0),
 display_name text NOT NULL,
 category text NOT NULL CHECK (category IN ('RETAIL','FOOD','SERVICES')),
 created_at timestamptz NOT NULL
);
CREATE TABLE payments.transactions (
 transaction_id bigint PRIMARY KEY CHECK (transaction_id > 0),
 card_id bigint NOT NULL REFERENCES payments.cards(card_id),
 account_id bigint NOT NULL REFERENCES payments.accounts(account_id),
 merchant_id bigint NOT NULL REFERENCES payments.merchants(merchant_id),
 amount numeric(15,2) NOT NULL CHECK (amount > 0),
 currency char(3) NOT NULL CHECK (currency = 'BRL'),
 status text NOT NULL CHECK (status IN ('APPROVED','DECLINED','REVERSED')),
 occurred_at timestamptz NOT NULL,
 created_at timestamptz NOT NULL,
 updated_at timestamptz NOT NULL CHECK (updated_at >= created_at),
 FOREIGN KEY (card_id, account_id) REFERENCES payments.cards(card_id, account_id)
);
CREATE INDEX accounts_customer_idx ON payments.accounts(customer_id);
CREATE INDEX cards_account_idx ON payments.cards(account_id);
CREATE INDEX transactions_account_idx ON payments.transactions(account_id);
CREATE INDEX transactions_merchant_idx ON payments.transactions(merchant_id);
CREATE INDEX transactions_card_time_idx ON payments.transactions(card_id, occurred_at);
COMMIT;
