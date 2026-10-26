-- DECISAO DO PROJETO - EXCECAO DE SEGURANCA PARA LABORATORIO.
-- Prerequisitos: logical replication ativa; cdc_user criado por Neon CLI/API/Console.
-- Neon concede privilegios amplos: estes GRANTs nao os restringem.
-- Senha somente runtime. Nao criar role administrativa nem slot aqui.
BEGIN;
DO $$ BEGIN
 IF current_setting('wal_level') <> 'logical' THEN
  RAISE EXCEPTION 'H03_REQUIRES_LOGICAL_WAL';
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='cdc_user' AND rolcanlogin) THEN
  RAISE EXCEPTION 'H03_CREATE_CDC_USER_VIA_NEON_FIRST';
 END IF;
END $$;
GRANT CONNECT ON DATABASE neondb TO cdc_user;
GRANT USAGE ON SCHEMA payments TO cdc_user;
GRANT SELECT ON payments.accounts, payments.cards, payments.transactions TO cdc_user;
ALTER TABLE payments.accounts REPLICA IDENTITY FULL;
ALTER TABLE payments.cards REPLICA IDENTITY FULL;
ALTER TABLE payments.transactions REPLICA IDENTITY FULL;
CREATE PUBLICATION bootcamp_cdc_pub
 FOR TABLE payments.accounts, payments.cards, payments.transactions
 WITH (publish = 'insert, update, delete');
COMMIT;
