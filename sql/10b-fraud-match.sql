-- MATCH PLANNER PASS — NOT RUN
-- C5 exact full query accepted; runner LAB_SA_1 / pool LAB_LFCP_2 / session UTC.
-- MATCH_SIZE_RUNTIME_VALIDATION_REQUIRED: 3/4/5 events; txn_count may exceed 3.
-- Strict boundary runtime cases 59.999/60.000/60.001s remain untested.
INSERT INTO `desafio.fraud.detected`
WITH fraud_matches AS (
  SELECT * FROM `desafio.transactions.fraud.events`
  MATCH_RECOGNIZE (
    PARTITION BY card_id
    ORDER BY event_time, transaction_id
    MEASURES
      COUNT(T.transaction_id) AS txn_count,
      FIRST(T.event_time) AS first_event_time,
      LAST(T.event_time) AS last_event_time,
      FIRST(T.transaction_id, 0) AS tx1_id,
      FIRST(T.event_time, 0) AS tx1_time,
      FIRST(T.amount, 0) AS tx1_amount,
      FIRST(T.transaction_status, 0) AS tx1_status,
      FIRST(T.transaction_id, 1) AS tx2_id,
      FIRST(T.event_time, 1) AS tx2_time,
      FIRST(T.amount, 1) AS tx2_amount,
      FIRST(T.transaction_status, 1) AS tx2_status,
      FIRST(T.transaction_id, 2) AS tx3_id,
      FIRST(T.event_time, 2) AS tx3_time,
      FIRST(T.amount, 2) AS tx3_amount,
      FIRST(T.transaction_status, 2) AS tx3_status
    ONE ROW PER MATCH
    AFTER MATCH SKIP TO NEXT ROW
    PATTERN (T{3,}?) WITHIN INTERVAL '60' SECOND
    DEFINE T AS TRUE
  )
)
SELECT SHA256(CONCAT(
         'RULE_VELOCITY-v1|CREATION_EVENT|', CAST(card_id AS STRING), '|',
         CAST(tx1_id AS STRING), ',', CAST(tx2_id AS STRING), ',',
         CAST(tx3_id AS STRING), '|',
         DATE_FORMAT(first_event_time,'yyyy-MM-dd HH:mm:ss.SSS'), '|',
         DATE_FORMAT(last_event_time,'yyyy-MM-dd HH:mm:ss.SSS'))) AS alert_id,
       'RULE_VELOCITY' AS rule_code,
       'RULE_VELOCITY-v1' AS rule_version,
       'CREATION_EVENT' AS semantic,
       card_id, txn_count, first_event_time, last_event_time,
       CAST(TIMESTAMPDIFF(MILLISECOND, first_event_time, last_event_time)
            AS BIGINT) AS interval_ms,
       tx1_id, tx1_time, tx1_amount, tx1_status,
       tx2_id, tx2_time, tx2_amount, tx2_status,
       tx3_id, tx3_time, tx3_amount, tx3_status
FROM fraud_matches
WHERE txn_count >= 3
  AND last_event_time < first_event_time + INTERVAL '60' SECOND;
