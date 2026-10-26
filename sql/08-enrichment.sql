-- DECISÃO DO PROJETO — SQL FLINK / TEMPO FLINK.
-- Statement property obrigatória: sql.tables.scan.idle-timeout = 5 s.
-- EXPLAIN obrigatório antes da submissão do INSERT.
-- DECISÃO DO PROJETO — H06 RECOVERY BASELINE (H06-H).
-- Somente recovery H06-E + CDC futuro; offsets iniciais INCLUSIVOS, partição 0.
-- Histórico H04/H05 preservado, fora deste scan. H06-G full replay continua histórico.
-- PLAN: não executar INSERT até autorização e resolução do bloqueio BASIC.
-- Novo snapshot durante runtime invalida o contrato: parar/revisar a boundary.
INSERT INTO `desafio-final`.`desafio-basic`.`desafio.transactions.enriched`
SELECT t.transaction_id, t.card_id, t.account_id, t.amount, t.currency,
       t.status AS transaction_status, t.occurred_at,
       a.status AS account_status, CAST(TO_TIMESTAMP_LTZ(t.occurred_at, 'yyyy-MM-dd''T''HH:mm:ss.SSSSSS''Z''', 'UTC') AS TIMESTAMP_LTZ(3)) AS event_time
FROM `desafio-final`.`desafio-basic`.`desafio.payments.transactions`
  /*+ OPTIONS(
    'scan.startup.mode'='specific-offsets',
    'scan.startup.specific-offsets'='partition:0,offset:2003'
  ) */ AS t
JOIN `desafio-final`.`desafio-basic`.`desafio.payments.accounts`
  /*+ OPTIONS(
    'scan.startup.mode'='specific-offsets',
    'scan.startup.specific-offsets'='partition:0,offset:242'
  ) */
  FOR SYSTEM_TIME AS OF t.`$rowtime` AS a
ON t.account_id = a.account_id;
