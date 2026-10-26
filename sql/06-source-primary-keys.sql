-- DECISÃO DO PROJETO — SQL FLINK. Executar separadamente e verificar após cada ALTER.
ALTER TABLE `desafio-final`.`desafio-basic`.`desafio.payments.accounts`
  ADD CONSTRAINT pk_h06_accounts PRIMARY KEY (account_id) NOT ENFORCED;

ALTER TABLE `desafio-final`.`desafio-basic`.`desafio.payments.transactions`
  ADD CONSTRAINT pk_h06_transactions PRIMARY KEY (transaction_id) NOT ENFORCED;
