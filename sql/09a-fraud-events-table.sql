-- APPLIED H07-C — DO NOT RE-RUN BLINDLY
-- Historical applied DDL; C4 catalog readback PASS. No DDL executed in C5.
CREATE TABLE `desafio.transactions.fraud.events` (
  transaction_id BIGINT NOT NULL,
  card_id BIGINT NOT NULL,
  account_id BIGINT NOT NULL,
  amount DECIMAL(15,2) NOT NULL,
  currency STRING NOT NULL,
  transaction_status STRING NOT NULL,
  occurred_at STRING NOT NULL,
  account_status STRING NOT NULL,
  event_time TIMESTAMP_LTZ(3) NOT NULL,
  WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND,
  PRIMARY KEY (transaction_id) NOT ENFORCED
)
DISTRIBUTED BY HASH(transaction_id) INTO 1 BUCKETS
WITH (
  'changelog.mode'='append',
  'key.format'='avro-registry',
  'value.format'='avro-registry',
  'kafka.cleanup-policy'='delete',
  'kafka.retention.time'='7 d'
);
