# Evidências acadêmicas selecionadas

Todos os JSONs usam wrapper `SANITIZED_HISTORICAL_SELECTION`, data histórica e origem no commit-base. IDs de infraestrutura são aliases; valores de negócio sintéticos foram preservados. Sem links para arquivos privados ausentes.

| Etapa | Arquivo | O que comprova / limite |
|---|---|---|
| H01 | [Acessos](../evidencias/H01/access-tests.json) | Quatro testes reais de ACL, permissões e negativas; tópico temporário de validação, não pipeline atual. |
| H02 | [Avro](../evidencias/H02/avro-compatibility.json) | V1/V2 reais, BACKWARD e V3 rejeitada; Pedido próprio separado de CDC. |
| H03 | [Banco](../evidencias/H03/database.json) | Seed e contagens sintéticas, privileges históricos/exceção CDC, não estado atual. |
| H04 | [Connector](../evidencias/H04/connector.json) | Readback/config históricos sanitizados; RUNNING somente no instante registrado. |
| H05 | [Consolidado CDC](../evidencias/01-envelopes-cdc.json) | Quatro eventos reais c/u/d/tombstone, before/after, key/partition/offset; original integral excluído. |
| H06 | [Enriquecimento](../evidencias/H06/enrichment.json) | Gate histórico/contagens/amostra temporal; committed atual NOT_PROVEN, sem replay integral das2000PKs. |
| H07 | [P1](../evidencias/H07/P1.json), [N1](../evidencias/H07/N1.json), [N2](../evidencias/H07/N2.json), [B1](../evidencias/H07/B1.json) | P1 causal real e SHA256; N1 PASS, N2 retrospectivo; B1 erro59999/59000. H07 PARTIAL. |
| H08 | [Segurança](../evidencias/H08/security.json), [Billing](../evidencias/H08/billing.json), [observabilidade](../evidencias/H08/observability.json) | ACLs/RBAC com aliases; custos reais e créditos organizacionais; métricas NOT_MEASURED, não zero. |

História original, run directories integrais, raw Avro/base64, identidade administrativa e endpoints reais não fazem parte deste pacote. A origem e os hashes estão no [manifesto](../release-manifest.json), auditáveis pelo proprietário contra o repositório privado. Sanitização implica que os bytes exportados não são os bytes integrais originais; nenhuma leitura Kafka ou coleta cloud foi repetida.
