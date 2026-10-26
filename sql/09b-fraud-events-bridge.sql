-- BRIDGE PLANNER PASS — NOT RUN
-- H07_RUNTIME_ACTIVATION_OFFSET MUST BE CAPTURED IMMEDIATELY BEFORE FIRST SUBMISSION
-- Replace the placeholder only after fresh partition/boundary checks and runtime authorization.
-- C4 planner evidence; runner LAB_SA_1 / pool LAB_LFCP_2 / session UTC.
INSERT INTO `desafio.transactions.fraud.events`
WITH h07_activation_source AS (
  SELECT *
  FROM `desafio.transactions.enriched`
  /*+ OPTIONS(
    'scan.startup.mode'='specific-offsets',
    'scan.startup.specific-offsets'='partition:0,offset:<H07_RUNTIME_ACTIVATION_OFFSET>'
  ) */
)
SELECT
  transaction_id,
  card_id,
  account_id,
  amount,
  currency,
  transaction_status,
  occurred_at,
  account_status,
  event_time
FROM TO_CHANGELOG(
  input => TABLE h07_activation_source,
  op => DESCRIPTOR(change_op),
  op_mapping => MAP['INSERT','INSERT']
);
