# Reconstrução manual e preparação local

Este pacote não tem `.git`, credenciais, capturas integrais, SDKs cloud ou helpers privados. Scripts incluídos só validam/preparam arquivos locais. Evidence files são SANITIZED_HISTORICAL_SELECTION, não provas de deploy deste pacote.

## Começar do zero

1. Descompactar/copiar o pacote em diretório novo; não sobrepor o laboratório existente. Usar Bash/Git Bash e Python 3.10+.
2. `bash harness/checks/verify.sh --strict-export` confere a seleção, hashes, links, privacidade e dados CDC/P1/B1/Billing sem rede.
3. `bash setup.sh --check` verifica as fontes; `bash setup.sh --prepare` cria `.env` somente se ausente e `.local/delivery/preparation.json`. Defaults do template não são credenciais. Targets symlink são recusados; não há flag deploy/apply.
4. Testes do setup: depois de preparar, `python -m unittest discover -s harness/checks -p 'test_h09_prepare.py'`. Arquivos `.env`/`.local` criados pelo usuário nunca devem ser redistribuídos; `--strict-export` rejeita a presença deles. Para conferir somente fontes após preparação: `bash harness/checks/verify.sh`.

Não é necessário instalar SDK para esses checks. requirements-offline.txt registra fastavro usado pelas auditorias privadas, mas o pacote selecionado não contém wire Avro bruto nem promete repeti-las integralmente. Nenhum pacote é instalado automaticamente.

## Etapas cloud futuras — não executadas pelo pacote

| Ordem | Arquivos e ação manual | Dependências/pré-condições |
|---|---|---|
| Fundação/Avro | Criar laboratório autorizado, contas de aplicação/ACLs; registrar schemas/pedido-v1/v2; testar V3 incompatível | CLI oficial, autenticação privada, orçamento/região/namespaces aprovados. Usar novos IDs, não aliases das evidências; V3 rejeitada é resultado esperado. |
| PostgreSQL | dataset/neon/sql/01_ddl.sql → 02_seed.sql → 03_cdc_setup.sql via cliente SQL com ON_ERROR_STOP | Banco novo sem payments, TLS/logical replication e role cdc_user aprovados; seed42/2000 transações sintéticas. Exceção neon_superuser deve ser explicitamente revista, não menor privilégio estrito. |
| CDC | Preencher privadamente placeholders de connectors/cdc.json e criar connector via CLI oficial | Publication/slot/FULL/tabelas/SSL e SA corretos. `${KAFKA_PRODUCER_SERVICE_ACCOUNT_ID}` deve receber a nova identidade. Config preenchida nunca é versionada. Snapshot inicial e recovery exigem correlação própria. |
| Enriquecimento | SQL06/07/08 com catalog/propriedades/PK/changelog/tempo/pool revisados | Canal Flink oficial e RBAC aprovados; validar inputs/outputs e integridade atual, não inferir de evidência histórica. |
| Fraude | SQL09a/09b/10a/10b com boundary nova e testes autorizados | Não copiar offset histórico; bridge contém placeholder deliberado. H07 tem gates pendentes, não supor prevenção universal de snapshots ou replay seguro. Preservar o erro B1 até correção comprovada por runtime. |
| Operação | Métricas/inventários/Billing oficiais somente sob autorização | Credencial Metrics apropriada e grupo elegível; as séries deste histórico NÃO foram medidas. Consumer→efeito requer idempotência própria, não implementada aqui. |

Exemplo futuro, **somente com nova autorização e banco novo**:

```bash
psql "$POSTGRES_URL" -v ON_ERROR_STOP=1 -f dataset/neon/sql/01_ddl.sql
psql "$POSTGRES_URL" -v ON_ERROR_STOP=1 -f dataset/neon/sql/02_seed.sql
psql "$POSTGRES_URL" -v ON_ERROR_STOP=1 -f dataset/neon/sql/03_cdc_setup.sql
confluent connect cluster create --config-file ARQUIVO_PRIVADO \
  --environment "$CONFLUENT_ENVIRONMENT_ID" --cluster "$CONFLUENT_CLUSTER_ID"
```

Os comandos acima não pertencem ao setup e não foram executados para este candidato. Os scripts cloud históricos, vinculados a scopes e campanhas do laboratório original, foram excluídos; o canal de submissão Flink e as pré-condições devem ser reconstruídos manualmente com aprovação. SQL íntegro do professor não foi recuperado: arquivos próprios do projeto, não uma automação oficial do curso.

## O que a auditoria consegue reproduzir

CDC before/after c/u/d/tombstone e offsets adjacentes; três entradas P1/INSERT/alerta e SHA256; limite B1 falho; totais Decimal de60 linhas Billing; respostas históricas selecionadas de fundação/Avro/enriquecimento. Não reconstrói 2000 linhas H06, wire Avro ou saúde atual cloud. Alterar um arquivo do pacote requer nova construção do manifesto, não apagar a falha do check.

H07/H08 continuam PARTIAL; H09 PARTIAL; H10 [planejado](10-checklist-encerramento.md), não executado. Publicação sanitizada autorizada em 26/10/2026; infraestrutura cloud e teardown não foram autorizados por essa decisão.
