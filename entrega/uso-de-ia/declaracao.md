# Declaração de uso de IA

## Ferramenta e modelos

Usei o **Claude Code** (Anthropic) como IA de apoio, em uma única sessão, exportada em `sessao.md`. Troquei de modelo conforme a etapa:

| Etapa | Modelo |
|---|---|
| Análise inicial do código e dos defeitos | Claude Sonnet 5.5 |
| Revisão das hipóteses, escrita do código e dos testes | Claude Opus 5.5 |
| Revisão final do projeto e do `README-ENTREGA.md` | Claude Fable 5.2 |

## O que eu fiz

- Defini as regras do trabalho: eu investigo primeiro e trago a hipótese; a IA não altera nada sem eu pedir; cada correção vem com um teste novo que falha antes e passa depois; um commit por mudança.
- Rodei a suíte e o CLI na amostra do README e levantei os sintomas (5 testes falhando, total e noites errados).
- Para cada defeito, reproduzi o erro, fiz a conta do valor esperado, abri o código e formulei a hipótese da causa e da correção antes de pedir qualquer alteração.
- No defeito de status, escrevi a correção e os três primeiros testes e fiz os dois commits.
- Revisei todo o código e todos os testes escritos pela IA antes de autorizar cada commit.
- Decidi o que ficava fora do escopo, como manter o código de saída `1` para moeda sem taxa.
- Escrevi o `README-ENTREGA.md`.

## O que a IA fez

- Leu o README e o código e fez a análise inicial dos defeitos. Foi ela que apontou o limite de 200 linhas na leitura do CSV, que nenhum teste fornecido pega.
- Confirmou ou contestou cada hipótese minha e apontou o que eu não tinha visto. Por exemplo: o teste fornecido de câmbio não pega o uso de `float`, e o de ranking passaria também com `reverse=True`.
- Avisou que o repositório remoto estava sem a base do projeto e fez esse commit a meu pedido.
- No status, revisou a minha correção e acrescentou dois testes.
- Nos defeitos de câmbio, noites, ranking e leitura, escreveu a correção e os testes, mostrou que os testes falhavam antes e passavam depois, e validou contra a amostra e o dataset completo.
- Fez os commits e os pushes desses defeitos, a meu pedido e depois da minha revisão.
- Fez a revisão final: clone limpo, contrato do CLI e casos de borda. Não encontrou defeito contra o README e listou os comportamentos fora do escopo.
- Revisou o `README-ENTREGA.md`, apontou trechos que não batiam com a sessão e aplicou os ajustes a meu pedido.
- Redigiu esta declaração a partir das informações que passei; eu revisei o texto.
