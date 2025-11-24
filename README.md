<h1 align="center">🔎 Conciliação de Transações (Subset Sum) — Gerador & Verificador (DP)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/Status-Ativo-success" />
  <img src="https://img.shields.io/badge/Plataforma-OS%20independente-8A2BE2" />
</p>

<p align="center">
  Gera instâncias realistas de transações (em centavos) e verifica, via Programação Dinâmica, se existe um subconjunto que soma exatamente um alvo 💰.
</p>

---

## 🗂️ Conteúdo
- [Visão geral](#-visão-geral)
- [Arquivos principais](#-arquivos-principais)
- [Formato do CSV](#-formato-do-csv)
- [Como usar (passo a passo)](#-como-usar-passo-a-passo)
- [Exemplos rápidos](#-exemplos-rápidos)
- [Boas práticas no Windows (caminhos)](#-boas-práticas-no-windows-caminhos)
- [Desempenho & limites](#-desempenho--limites)
- [Estrutura sugerida do repositório](#-estrutura-sugerida-do-repositório)
- [Dúvidas frequentes (FAQ)](#-dúvidas-frequentes-faq)
- [Licença](#-licença)
- [LINK DO YOUTUBE](#-link-do-youtube)

---

## 🌟 Visão geral
Este repositório traz dois utilitários complementares:

1. **Gerador Interativo (Mix)** — `make_instances_interativo_mix.py`  
   - Você informa **alvo** (centavos ou em reais, ex.: `68674,67`), **N** (nº transações) e **onde salvar** o `.csv`;
   - **Sem perguntas extras**: o script decide **aleatoriamente** se a instância terá **solução** (solvable) **ou não** (unsat).
   - Ideal para **testar** seu verificador em cenários variados.

2. **Verificador (DP Subset Sum)** — `subset_sum_dp_verifica_csv.py`  
   - Lê o `.csv` e checa, via **DP (bitset) + reconstrução**, se existe subconjunto que soma **exatamente** o alvo;
   - Imprime **ENCONTRADO** (com a lista de valores) ou **NÃO ENCONTRADO**.

> 💡 **Motivação**: modela conciliação/auditoria de transações (ex.: detectar conjunto que fecha um valor exato).

---

## 🔧 Arquivos principais

| Arquivo | Descrição |
|---|---|
| `make_instances_interativo_mix.py` | Gerador de **uma** instância `.csv` (solvável **ou** inviável, escolhido aleatoriamente). |
| `subset_sum_dp.py` | Verificador **Subset Sum** com **DP (bitset)** e **reconstrução do subconjunto**. |
| `README.md` | Este documento. |

> 📎 **Exemplos prontos (opcionais)**  
> - [teste.csv]> - ---

## 📄 Formato do CSV

**Cabeçalho obrigatório:**
```csv
name,pool,target


name: rótulo da instância (livre).

pool: lista de inteiros (centavos) entre colchetes, ex.: [90,50025,1500,71410].
(O verificador também aceita 1,2,3 ou 1;2;3, mas recomendamos colchetes).

target: inteiro (centavos).

Exemplo:

name,pool,target
custom_solvable_280,"[90,50025,1500,71410,9999,2021]",123456

▶️ Como usar (passo a passo)
1) Gerar uma instância (mix: pode ter solução ou não)

Não há mais perguntas sobre subconjunto — apenas ALVO, N e onde salvar.

python "C:/caminho/para/make_instances_interativo_mix.py"
# Alvo — CENTAVOS (ex.: 6867467) OU REAIS (ex.: 68674,67): 7358450,23
# Número de transações a gerar (ex.: 30000): 280
# Salvar em: "C:/Users/voce/Documentos/transacoes.csv"

2) Verificar a instância gerada (DP Subset Sum)

Com argumento:

python "C:/caminho/para/subset_sum_dp_verifica_csv.py" "C:/Users/voce/Documentos/transacoes.csv"


Sem argumento (o script pedirá o caminho):

python "C:/caminho/para/subset_sum_dp_verifica_csv.py"
# Caminho do CSV: C:/Users/voce/Documentos/transacoes.csv

⚡ Exemplos rápidos
<details> <summary><strong>Saída esperada: ENCONTRADO</strong></summary>
================================================================================
Instância: custom_solvable_280
Alvo  : 735845023 -> R$ 7.358.450,23
Itens : 280 valores

>>> ENCONTRADO
Soma do subconjunto: 735845023 -> R$ 7.358.450,23
Subconjunto (centavos): [ ... ]
Subconjunto (R$)      : ['R$ 12.345,67', 'R$ 98.765,43', ...]

</details> <details> <summary><strong>Saída esperada: NÃO ENCONTRADO</strong></summary>
================================================================================
Instância: custom_unsat_120
Alvo  : 450093 -> R$ 4.500,93
Itens : 120 valores

>>> NÃO ENCONTRADO

</details>
🪟 Boas práticas no Windows (caminhos)

⚠️ Muito importante:

Use barras / nos caminhos e coloque entre aspas;

Evite \ (pode virar escape \U...).

✅ Correto

"C:/Users/voce/Documentos/transacoes.csv"


❌ Evite

C:\Users\voce\Documentos\transacoes.csv


Se editar o caminho dentro do código, prefira:

from pathlib import Path
out = Path("C:/Users/voce/Documentos/transacoes.csv")   # OK
# ou
out = Path(r"C:\Users\voce\Documentos\transacoes.csv")  # raw string OK

🧮 Desempenho & limites

O verificador usa DP com bitset; o custo cresce com o alvo em centavos (T).

Para alvos muito grandes (ex.: centenas de milhões de centavos), pode haver consumo elevado de memória/tempo.

Dica: usar alvos moderados (até alguns milhões de centavos) e N na casa de centenas.

🧱 Estrutura sugerida do repositório
/
├─ make_instances_interativo_mix.py      # gerador (uma instância; solvável/insucesso aleatório)
├─ subset_sum_dp_verifica_csv.py         # verificador (DP + reconstrução do subconjunto)
├─ README.md
    └─ LINK DO VIDEO NO YOUTUBE
├─ PDF dos slides

❓ Dúvidas frequentes (FAQ)

1) Posso digitar o alvo como “R$ 1.234,56”?
Sim. O gerador aceita centavos (123456) ou reais (1234,56 / R$ 1.234,56).

2) Por que minha instância deu “NÃO ENCONTRADO”?
Porque o gerador mistura casos solváveis e inviáveis (por construção modular). Isso é intencional para testar o verificador.

3) Quero controlar a proporção de casos com/sem solução.
A versão atual decide 50/50 internamente. Se quiser, é simples expor um parâmetro (ex.: p_solv).

🧭 Fluxo (alto nível)
flowchart LR
  A[Usuário informa Alvo & N] --> B[Gerador Interativo (Mix)]
  B -->|CSV: name,pool,target| C[Verificador (DP Subset Sum)]
  C --> D{Existe subconjunto?}
  D -->|Sim| E[ENCONTRADO: imprime valores]
  D -->|Não| F[NÃO ENCONTRADO]

📜 Licença

Defina a licença que preferir (ex.: MIT ou Apache-2.0).

<p align="center"> <i>Contribuições, issues e PRs são bem-vindos! 🚀</i> </p> ```

▶️ LINK DO YOUTUBE

<https://www.youtube.com/watch?v=_6205XkHYQI>
