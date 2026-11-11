# Entrega: consolidador de reservas de hotel

O CLI gerava números errados. Corrigi 5 defeitos, cada um com teste novo, sem alterar os testes fornecidos nem os CSVs de `data/`.

## Defeitos corrigidos

| # | Defeito | Causa raiz | Arquivo | Commits (teste, correção) |
|---|---|---|---|---|
| 1 | Reservas `NO_SHOW` entravam nos totais | `is_billable` usava `!= "CANCELLED"` em vez de aceitar só `CONFIRMED` | `services/status_policy.py` | `b6ed14b`, `b116500`; testes extras: `a7e0f5e`, `93777ab` |
| 2 | Valores em moeda estrangeira errados | A conversão dividia pela taxa, usando `float`, em vez de `amount * rate` em `Decimal` | `services/currency_converter.py` | `ee6b070`, `c4274d9` |
| 3 | Noites negativas na virada de mês | O cálculo subtraía `checkout.day - checkin.day` em vez da diferença entre as datas | `services/stay_calculator.py` | `b13adf3`, `f70fbf5` |
| 4 | `top_hotels` do menor para o maior valor | `sorted` ascendente; o certo é valor decrescente e `hotel_id` ascendente no empate | `services/report_builder.py` | `859e91e`, `cb3346a` |
| 5 | 100 reservas ignoradas na leitura | Um `break` interrompia a leitura do CSV ao chegar em 200 linhas | `repositories/csv_reservation_repository.py` | `3fc1bc2`, `d341b0d` |

## Como investiguei

A análise inicial dos defeitos foi feita com a ajuda da IA. Depois, para cada defeito, reproduzi o erro pelo teste ou pelo CLI, calculei o valor esperado, abri o código e formulei a minha hipótese.

Com a hipótese pronta, enviei para a IA para verificar se estava correta ou se eu tinha deixado passar alguma coisa. Quase sempre eu havia deixado escapar algum detalhe em que não tinha pensado. No defeito de status, eu mesmo escrevi a correção e os três primeiros testes e fiz os dois commits; a IA revisou e acrescentou dois testes depois. Nos outros quatro defeitos, pedi à IA que escrevesse o código e os testes. Revisei tudo para conferir se estava de acordo com o que eu queria propor e, só depois da minha revisão, pedi a ela que fizesse os commits e os pushes.

O limite de 200 linhas nenhum teste fornecido pega. A IA apontou o `break` ao ler o código na análise inicial, e confirmei rodando o CLI no dataset completo, que mostrava 200 reservas em vez de 300.

Ao final, pedi uma revisão a um modelo mais capaz da IA. Ela não encontrou nenhum defeito contra as regras do README e apontou os comportamentos descritos na seção seguinte.

## Como validar

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

- **Amostra** (`data/exemplo-validacao.csv`): 28 noites, 7566.00 BRL e média 270.21, igual à tabela do README do desafio.
- **Dataset completo**: 300 reservas (235 confirmadas, 31 canceladas, 34 no-show), 1347 noites, 396170.00 BRL e média 294.11. Conferi contra uma conta independente feita direto sobre o CSV.

Observação: a soma dos `total_brl` de `by_month` dá 396170.01, um centavo acima do total. Cada mês é arredondado separadamente na serialização, e o total é arredondado uma única vez sobre a soma exata, como o desafio pede.

## Fora do escopo (observado, não alterado)

O README do desafio diz que os dados fornecidos estão consistentes. Os casos abaixo só acontecem com entradas inválidas, que não existem nos CSVs fornecidos, e por isso não os alterei. Testei cada um rodando o CLI:

| Entrada | O que acontece hoje |
|---|---|
| Moeda sem taxa na tabela (ex.: `GBP`) em reserva `CONFIRMED` | Sai com código `1` e `KeyError`; pelo contrato, entrada inválida deveria sair com `2` |
| Moeda em minúsculas (`usd`) | Mesmo `KeyError`: a tabela de taxas normaliza para maiúsculas, a reserva não |
| Valor `NaN` | Com um hotel, sai com código `0` e o resumo mostra `Total BRL: NaN`; com mais de um, sai com código `1` (`InvalidOperation` na ordenação do ranking) |
| Status desconhecido (ex.: `PENDING`) ou em minúsculas | Entra em `total_reservations`, mas em nenhuma das três contagens por status |
| Checkout antes do check-in | Gera noites negativas, sem aviso |
| Checkout no mesmo dia do check-in | Zero noites |
| CSV com BOM (exportado do Excel) | Sai com código `2`, mas a mensagem diz que falta a coluna `reservation_id` |
| `--output` apontando para um diretório | Sai com código `1`; o contrato não cobre esse caso |

O caso mais relevante é o da moeda sem taxa, porque o contrato fala em código `2` para entrada inválida. Como o README garante que todas as moedas do dataset têm taxa, deixei como está e registrei aqui.

## Resultado do pytest

Antes das correções: `5 failed`. Depois:

```
21 passed
```

São os 5 testes fornecidos e 16 novos, em `tests/test_fix_*.py`.
