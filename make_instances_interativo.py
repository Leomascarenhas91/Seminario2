#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador interativo de instância Subset Sum (CSV):
- Pede o ALVO (em centavos OU em reais BR: ex. 6867467 ou 68674,67)
- Pede o NÚMERO DE TRANSAÇÕES (N)
- Pede ONDE SALVAR o .csv (caminho completo)
- Gera N valores distintos (centavos) e garante um subconjunto que soma o ALVO

Observações:
- Não pergunta nada sobre “subconjunto”: o solver é quem encontra (ou não) a combinação.
- Método robusto: subset base = 1,2,3,...,k (centavos); último valor = T - sum(1..k).
  Ajustamos k para que o último valor seja > k (evita colisão) e positivo.
"""

import re
import csv
from pathlib import Path
from typing import List, Tuple

# -----------------------------
# Entrada do usuário (parsers)
# -----------------------------

def parse_target_to_centavos(user_input: str) -> int:
    """
    Converte a entrada do usuário para centavos (int).

    Aceita:
      1) SOMENTE DÍGITOS -> já em CENTAVOS
         Ex.: "6867467"  (6.867.467 centavos = R$ 68.674,67)

      2) Formato em REAIS (BR), com vírgula decimal e pontos opcionais de milhar:
         "68674,67"  |  "R$ 68.674,67"  |  "68.674,67"
    """
    s = user_input.strip()

    # Caso 1: apenas dígitos => já está em centavos
    if re.fullmatch(r"\d+", s):
        return int(s)

    # Caso 2: reais BR (R$ opcional, ponto milhar, vírgula decimal)
    s = re.sub(r"(?i)r\$\s*", "", s)  # remove "R$"
    s = s.replace(".", "")            # remove separador de milhar
    s = s.replace(",", ".")           # vírgula -> ponto
    try:
        valor = float(s)
        centavos = int(round(valor * 100))
        if centavos <= 0:
            raise ValueError("O alvo deve ser positivo.")
        return centavos
    except Exception:
        raise ValueError(
            "Alvo inválido. Digite em CENTAVOS (ex.: 6867467) ou em REAIS (ex.: 68674,67 ou R$ 68.674,67)."
        )

def ask_positive_int(prompt: str, min_value: int = 1) -> int:
    while True:
        s = input(prompt).strip()
        if not s.isdigit():
            print("Por favor, digite um número inteiro não negativo.")
            continue
        v = int(s)
        if v < min_value:
            print(f"Por favor, informe um valor >= {min_value}.")
            continue
        return v

def ask_output_path(prompt: str) -> Path:
    """
    Pergunta um caminho completo (incluindo o nome do arquivo .csv).
    Cria as pastas se necessário.
    """
    while True:
        p = input(prompt).strip().strip('"').strip("'")
        if not p:
            print("Caminho vazio. Tente novamente.")
            continue
        out = Path(p)
        if out.suffix.lower() != ".csv":
            print("O arquivo deve ter extensão .csv. Ex.: C:/pasta/instances_30k.csv")
            continue
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            return out
        except Exception as e:
            print(f"Não foi possível preparar a pasta: {e}. Tente outro caminho.")

# -----------------------------
# Núcleo robusto (sempre fecha T)
# -----------------------------

def triangular_sum(k: int) -> int:
    """Soma 1+2+...+k."""
    return k * (k + 1) // 2

def build_pool_with_solution(target: int, n: int) -> Tuple[List[int], int, List[int]]:
    """
    Constrói N valores distintos (centavos) com um subconjunto que soma 'target'.
    Estratégia determinística e robusta:
      - Escolhe k tal que sum(1..k) < target e (target - sum(1..k)) > k
      - Subconjunto = [1, 2, ..., k, last], onde last = target - sum(1..k)
      - Completa a pool até N com inteiros distintos > last
    Garante solução para qualquer T >= 1 e N >= 2.
    """
    if target <= 0:
        raise ValueError("target deve ser positivo (em centavos).")
    if n < 2:
        raise ValueError("N deve ser >= 2.")

    # Encontra o maior k com sum(1..k) < target
    k = 1
    while triangular_sum(k + 1) < target:
        k += 1
        if k > n - 1:  # não pode ultrapassar o limite (precisamos deixar 1 slot para 'last')
            break

    # Garante que temos espaço: k <= n-1
    if k > n - 1:
        k = n - 1

    # Ajusta k para garantir last > k
    # last = target - sum(1..k)  precisa ser > k  (para não colidir com 1..k)
    while True:
        s = triangular_sum(k)
        last = target - s
        if last > k and last > 0:
            break
        k -= 1
        if k < 1:
            # fallback mínimo: subset = [1, target-1] (target >= 2)
            if target <= 1:
                # caso extremo target=1 => subset=[1]
                subset = [1]
                used = {1}
                pool = list(subset)
                x = 2
                while len(pool) < n:
                    if x not in used:
                        pool.append(x); used.add(x)
                    x += 1
                return pool, target, subset
            subset = [1, target - 1]
            used = set(subset)
            pool = list(subset)
            x = max(subset) + 1
            while len(pool) < n:
                if x not in used:
                    pool.append(x); used.add(x)
                x += 1
            return pool, target, subset

    # Agora temos k >= 1, last > k, ambos positivos e distintos
    subset = list(range(1, k + 1)) + [last]
    used = set(subset)

    # Completa a pool com valores distintos > last
    pool = list(subset)
    x = last + 1
    while len(pool) < n:
        if x not in used:
            pool.append(x); used.add(x)
        x += 1

    return pool, target, subset

# -----------------------------
# Execução principal
# -----------------------------

def main():
    print("=== Gerador de Instância Subset Sum (CSV) — Modo Interativo ===\n")

    # Alvo (claro e direto)
    # -> Em CENTAVOS: ex.: 6867467     (interpreta como R$ 68.674,67)
    # -> Em REAIS:    ex.: 68674,67    (ou: R$ 68.674,67)
    while True:
        try:
            alvo_str = input("Alvo (em CENTAVOS, ex.: 6867467) OU em REAIS (ex.: 68674,67): ")
            target = parse_target_to_centavos(alvo_str)
            break
        except ValueError as e:
            print(e)

    # Número de transações
    n = ask_positive_int("Número de transações a gerar (ex.: 30000): ", min_value=2)

    # Onde salvar
    print("\nInforme o caminho COMPLETO do arquivo .csv de saída.")
    print("Ex.: C:/Users/seu_usuario/Documentos/instances_30k.csv")
    out_path = ask_output_path("Salvar em: ")

    # Gera pool + subset garantido
    pool, T, subset = build_pool_with_solution(target=target, n=n)

    # Escreve CSV
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "pool", "target"])
        pool_str = "[" + ",".join(str(x) for x in pool) + "]"
        w.writerow([f"custom_{n}", pool_str, str(T)])

    # Resumo
    print("\n=== Concluído ===")
    print("Arquivo salvo em:", out_path.resolve())
    print("Tamanho da pool:", len(pool))
    print("Distintos?      ", len(set(pool)) == len(pool))
    print("Soma(subset)==T:", sum(subset) == T)
    print("Exemplo de subconjunto garantido (tamanhos pequenos):",
          subset if len(subset) <= 12 else (subset[:10] + ["...", subset[-1]]))
    print("Alvo (R$):      ", f"R$ {T/100:.2f}".replace(".", ","))

if __name__ == "__main__":
    main()
