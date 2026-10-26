# Fraude — demonstração real sanitizada

Fonte do curso: três transações de um cartão em intervalo inferior a 60 s, MATCH_RECOGNIZE/RULE_VELOCITY, alerta e três testemunhas. SQL10b é próprio, usado historicamente; seu cabeçalho NOT RUN refere-se ao checkpoint de planejamento anterior. Padrão T{3,}?/WITHIN60s, PARTITION BY card_id, filtro estrito e testemunhas no [SQL](../sql/10b-fraud-match.sql).

**H07 PARTIAL — ACADEMIC CORE EVIDENCED; Fraud Gate NOT_PROVEN.** [P1](../evidencias/H07/P1.json): card_id1, IDs102001/102002/102003, 07/10/2026 UTC11:49:04.626/24.626/44.626, BRL10.11/11.11/12.11, APPROVED/DECLINED/REVERSED, txn_count3 e interval_ms40000. INSERT confirmado → três criações → alerta Kafka real, testemunhas e SHA256 íntegros.

O polling inicial foi interrompido antes do advancer planejado; o alerta foi observado tardiamente após cleanup. Causa/momento do avanço do watermark não estabelecidos; positivo acadêmico não aprova todo o cenário operacional. A seleção pública preserva valores decodificados, offset e observação, mas exclui raw Avro/base64. Seu checker recomputa SHA256 e correspondência às entradas, sem afirmar replay integral do wire.

[N1](../evidencias/H07/N1.json) PASS: duas transações, advancer separado e captura histórica, sem alerta novo. [N2](../evidencias/H07/N2.json) PASS_RETROSPECTIVE: cards distintos e leitura histórica até high; não prova telemetria contínua nem conclusão do polling originalmente interrompido.

[B1](../evidencias/H07/B1.json) **FAIL_INTERVAL_PRECISION_HISTORICAL**: real59999ms, publicado59000ms, testemunhas/SHA256 corretos. Alerta preservado, não corrigido no pacote. Gates limites60000/60001, overlap4/5, UPDATE/recovery, H06 committed, snapshots e streaming candidato pendentes. Valores candidata18/18 e planner aceito foram provas separadas, não correção implantada; gate numérico formal incompleto. Snapshots repetidos readmitiram baseline; exactly-once ponta a ponta não demonstrado.

Roteiro para futura gravação: arquitetura → dataset/CDC → Kafka/Avro → SQL08 → SQL10b → P1 e testemunhas → negativos/B1/limites. Usar estes arquivos como evidência histórica, não screenshots atuais fabricados. Vídeo ainda não entregue.
