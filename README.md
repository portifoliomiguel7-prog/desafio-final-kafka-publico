# Pagamentos em tempo real — Projeto Final DIO

**Entrega sanitizada.** Publicação autorizada pelo proprietário em 26/10/2026 para [portifoliomiguel7-prog/desafio-final-kafka-publico](https://github.com/portifoliomiguel7-prog/desafio-final-kafka-publico). O repositório original permanece privado. H09 PARTIAL — PUBLIC_RELEASE_CANDIDATE_PREPARED; H10 PENDING. As evidências são seleções históricas reais, identificadas como sanitizadas, não novas execuções.

Objetivo: PostgreSQL → CDC/Debezium → Kafka/Avro → Flink SQL/temporal join → MATCH_RECOGNIZE → alerta RULE_VELOCITY, com três transações do mesmo cartão em menos de 60 segundos. Tecnologias do laboratório: PostgreSQL 17/Neon, Confluent Cloud Kafka/PostgresCdcSourceV2, Schema Registry/Avro, Flink SQL, Python/fastavro e Bash.

## Por que estas peças

PostgreSQL mantém o modelo relacional dos pagamentos; Neon foi o serviço gerenciado escolhido para o laboratório. Debezium/CDC captura snapshot e mudanças do WAL, preservando before/after. Kafka separa ingestão e processamento em tópicos com retenção para inspeção. Avro/Schema Registry torna os contratos e sua evolução verificáveis. Flink SQL permite expressar o enriquecimento temporal e a correlação por cartão em SQL versionado. Serviço gerenciado reduz a administração local, mas connector/Flink tiveram custos medidos e continuam exigindo controle operacional.

## Navegação

- [Índice de evidências H01–H08](docs/09-indice-evidencias.md)
- [Configuração e reprodução manual](docs/08-reproducao-entrega.md)
- [Fraude P1, negativos e B1](docs/07-demonstracao-fraude.md)
- [Operação e custos](docs/06-operacao.md)
- [Checklist humano](CHECKLIST.md) e [encerramento futuro](docs/10-checklist-encerramento.md)
- [Manifesto de arquivos, origem e transformações](release-manifest.json)

## Verificação local

Git Bash/Bash e Python 3.10+ são suficientes; não há Git history neste pacote. Antes de configurar credenciais:

```bash
bash harness/checks/verify.sh --strict-export
bash setup.sh --check
```

`bash setup.sh --prepare` cria somente `.env` ausente e manifesto local ignorado; preserva configuração existente. Não instala dependências ou provisiona serviços. [Guia](docs/08-reproducao-entrega.md) explica o caminho manual cloud; reprodução automática completa **não comprovada**. O SQL/dataset são arquivos reais do projeto; configurações de identidade são placeholders, jamais IDs prontos para usar.

## Resultados e limites

P1 real: IDs102001/102002/102003, card_id1, BRL10.11/11.11/12.11, APPROVED/DECLINED/REVERSED, 40000ms e txn_count3. O alerta preserva as três testemunhas e SHA256; foi observado tardiamente após interrupção do polling. N1 PASS e N2 PASS_RETROSPECTIVE. **H07 PARTIAL — ACADEMIC CORE EVIDENCED**, Fraud Gate NOT_PROVEN. B1 intervalo real59999ms/publicado59000ms: **FAIL_INTERVAL_PRECISION_HISTORICAL**. Limites60.000/60.001, overlap4/5, UPDATE/recovery e H06 committed atual pendentes; snapshots repetidos readmitiram baseline. Nenhuma garantia exactly-once ponta a ponta.

**H08 PARTIAL — Metrics NOT_MEASURED.** Billing UTC [2026-10-02,2026-10-14): USD 254.0597 uso e créditos organizacionais USD -254.0599; residual CLI USD -0.0002 preservado, **não é fatura final**. Custos recentes estavam parciais; capacidade não equivale a fatura. Received_bytes/lag não medidos, sem declarar ausência como zero.

## Privacidade, proveniência e encerramento

Emails, paths pessoais, identidades administrativas e localizadores reais foram excluídos ou substituídos. Identificadores sintéticos de negócio, valores, tempos e hashes de alertas permanecem para conferir a semântica. Raw Avro/base64 e investigações extensas foram excluídos; a auditoria pública verifica valores decodificados e não substitui a captura integral privada. O manifesto distingue cópia, seleção e sanitização, com hashes da fonte no commit-base e dos arquivos exportados; isso não é assinatura criptográfica de autoria.

Originais do curso não são distribuídos. O requisito acadêmico vem dos resumos de PDF p.1–2/DOCX P013/P014/P038/P034–P045 consultados no projeto; SQL integral e decisões de harness são próprios, não atribuídos ao professor. Não foi alegada análise do vídeo do professor. A apresentação própria foi gravada e narrada em sete cenas em 24/10/2026, com 630,165 segundos e 31 blocos de fala. [Validação local de arquivos](evidencias/H09/video-validation.json), revisada em 26/10/2026. A mídia não está incluída nem publicada neste pacote; a revisão editorial permanece pendente. A captura mostra CDC Failed, snapshot e alerta P1 histórico; não comprova uma nova execução ponta a ponta.

Teardown apenas planejado; teardown.sh mantém LOCKED/exit1. A autorização de publicação cobre somente esta seleção sanitizada no destino indicado. Novas permissões, infraestrutura, teardown e publicação de mídia exigem escopo próprio. H09 não está DONE.
