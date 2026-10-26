# Operação — resultados históricos sanitizados

**H08 PARTIAL — Metrics NOT_MEASURED**, preservado. [Descriptors/limites](../evidencias/H08/observability.json): received_bytes e consumer_lag_offsets conhecidos, nenhuma série real consultada. Ausência de grupos/métrica não é zero; assign() manual não comprova lag de grupo. Nenhuma nova investigação Metrics/Billing realizada para este pacote.

[Billing](../evidencias/H08/billing.json): UTC[2026-10-02,2026-10-14),60 linhas retornadas, **USD 254.0597 uso**, créditos **organizacionais USD -254.0599**, descontos0 e residual CLI USD -0.0002. IDs associados aos recursos foram substituídos por aliases consistentes; preço/amount/datas ficaram intactos. Não é fatura final, pagamento ou custo Neon; atualização até72h, dia13 parcial. Connector e Flink foram maiores componentes. Reduzir horas desnecessárias do connector e concentrar testes Flink são propostas; economia efetiva não medida.

[Segurança](../evidencias/H08/security.json): producer WRITE/CREATE/DESCRIBE, consumer READ/DESCRIBE em namespaces separados; runner EnvironmentAdmin/FlinkDeveloper. cdc_user Neon conserva exceção ampliada (neon_superuser/REPLICATION/CREATEDB/CREATEROLE/BYPASSRLS e DML efetivo histórico), sem menor privilégio estrito. Sem alteração de privilégios no candidato.

| Elo | Entrega/replay/falha/recuperação | Limite |
|---|---|---|
| PostgreSQL→CDC | Commit/WAL/slot e recovery when_needed | Snapshot repetido pode republicar baseline; offset indisponível foi observado no projeto. |
| CDC→Kafka | Envelopes r/c/u/d/tombstone; log retido permite releitura | Prefixo removido/retensão limitam reconstrução; offset não é contagem de mensagens. |
| Kafka→Flink | Changelog/temporal join/MATCH; retomadas históricas | Bridge readmitiu baseline; PK NOT ENFORCED não deduplica universalmente; H06 committed NOT_PROVEN. |
| Flink→Consumer | Alerta Kafka com testemunhas/hash, auditores por assign() | Seleção confirma P1/B1, não efeito externo em produção. |
| Consumer→Efeito | Reprocessamento pode repetir efeito | Idempotência própria/reconciliação não comprovadas; SHA256 sozinho não garante exactly-once. |

Nenhuma nova funcionalidade, deploy, resize, stop ou teardown. [Encerramento](10-checklist-encerramento.md) é somente planejamento.
