-- DECISÃO DO PROJETO — SQL FLINK. CREATE explícito; não CTAS.
CREATE TABLE `desafio-final`.`desafio-basic`.`desafio.transactions.enriched` (
  transaction_id BIGINT NOT NULL,
  card_id BIGINT NOT NULL,
  account_id BIGINT NOT NULL,
  amount DECIMAL(15,2) NOT NULL,
  currency STRING NOT NULL,
  transaction_status STRING NOT NULL,
  occurred_at STRING NOT NULL,
  account_status STRING NOT NULL,
  event_time TIMESTAMP_LTZ(3) NOT NULL,
  CONSTRAINT pk_h06_enriched PRIMARY KEY (transaction_id) NOT ENFORCED
)
DISTRIBUTED BY HASH(transaction_id) INTO 1 BUCKETS
WITH (
  'changelog.mode' = 'retract',
  'key.format' = 'avro-registry',
  'value.format' = 'avro-registry',
  'kafka.retention.time' = '7 d',
  'kafka.cleanup-policy' = 'delete'
);
