# Checklist da entrega sanitizada

- [ ] Ler README e reconhecer H07/H08/H09 PARTIAL, B1 precisão FAIL e Metrics NOT_MEASURED.
- [ ] Conferir manifesto/allowlist, origens e hashes com acesso autorizado ao repositório privado; seleção sanitizada não é captura integral nem assinatura de autoria.
- [ ] Inspecionar manualmente documentos/JSONs/dataset sintético e confirmar ausência de PII, secrets, endpoints reais, Git history, materiais originais e artefatos locais.
- [ ] Rever resultados dos testes/checker e limitações do scan. Ferramenta independente só é usada se disponível; ausência deve constar no relatório, sem prometer detecção universal.
- [ ] Não distribuir `.env`/`.local` eventualmente gerados durante a própria reprodução. Rodar `bash harness/checks/verify.sh --strict-export` antes de qualquer redistribuição.
- [ ] Rever direitos dos resumos/referências do curso; originais PDF/DOCX/MP4 não estão incluídos.
- [ ] Confirmar entendimento de que setup é local e cloud manual exige novas credenciais/IDs/autorizações e revisão de semântica.
- [ ] Revisar a apresentação histórica já gravada/narrada em sete cenas e decidir formato/link da entrega. Vídeo não está incluído; metadados locais não substituem publicação da mídia nem nova execução cloud.
- [x] Proprietário autorizou em 26/10/2026 a publicação da seleção sanitizada em [portifoliomiguel7-prog/desafio-final-kafka-publico](https://github.com/portifoliomiguel7-prog/desafio-final-kafka-publico), preservando o original privado. Essa autorização não inclui mídia, referência de voz, histórico privado ou recursos cloud.
- [ ] Autorizar H10 separadamente. Teardown continua planejado e bloqueado.

Pacote é candidato local, não certificado para exposição automática. Se algum dado inseguro for encontrado: BLOCKED, registrar somente caminhos e corrigir a seleção sem alterar os originais.
