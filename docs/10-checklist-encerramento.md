# H10 — checklist planejado

**H10 PENDING / PLANNED_NOT_EXECUTED.** teardown.sh mantém LOCKED/exit1. Nenhum recurso real é identificado por ID neste pacote; aliases não podem ser usados para remoção.

Após autorização H10 específica: confirmar identidade/ownership e inventário contemporâneo, preservar provas/Billing/vídeo e resolver recursos compartilhados antes de remover alvos próprios. Ordem proposta: cessar entrada → connector/CDC → statements Flink próprios → pool → tópicos/subjects próprios → chaves/ACLs/bindings/SAs → cluster/environment próprios → slot/publication/role/banco Neon próprios → configuração privada e Billing final.

Riscos: perda de histórico/checkpoints, replay/duplicatas, WAL acumulando com slot parado, revogação de acesso compartilhado e exclusão irreversível. Validar cada etapa com listagem/describe scoped e UTC; delete bem-sucedido não basta. Gate exige inventário final sem alvos e preservação de recursos alheios. Nenhuma remoção foi executada, nem execução futura aprovada por este checklist. STOP.
