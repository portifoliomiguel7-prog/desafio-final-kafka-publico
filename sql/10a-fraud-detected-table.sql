-- APPLIED H07-C — DO NOT RE-RUN BLINDLY
-- Historical applied DDL; C4 catalog readback PASS. No DDL executed in C5.
CREATE TABLE `desafio.fraud.detected` (
  alert_id STRING NOT NULL,
  rule_code STRING NOT NULL,
  rule_version STRING NOT NULL,
  semantic STRING NOT NULL,
  card_id BIGINT NOT NULL,
  txn_count BIGINT NOT NULL,
  first_event_time TIMESTAMP_LTZ(3) NOT NULL,
  last_event_time TIMESTAMP_LTZ(3) NOT NULL,
  interval_ms BIGINT NOT NULL,
  tx1_id BIGINT NOT NULL, tx1_time TIMESTAMP_LTZ(3) NOT NULL,
  tx1_amount DECIMAL(15,2) NOT NULL, tx1_status STRING NOT NULL,
  tx2_id BIGINT NOT NULL, tx2_time TIMESTAMP_LTZ(3) NOT NULL,
  tx2_amount DECIMAL(15,2) NOT NULL, tx2_status STRING NOT NULL,
  tx3_id BIGINT NOT NULL, tx3_time TIMESTAMP_LTZ(3) NOT NULL,
  tx3_amount DECIMAL(15,2) NOT NULL, tx3_status STRING NOT NULL,
  PRIMARY KEY (alert_id) NOT ENFORCED
)
DISTRIBUTED BY HASH(alert_id) INTO 1 BUCKETS
WITH (
  'changelog.mode'='append',
  'key.format'='avro-registry',
  'value.format'='avro-registry',
  'kafka.cleanup-policy'='delete',
  'kafka.retention.time'='7 d'
);
