#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subset Sum (DP com bitset + reconstrução) que LÊ um CSV e imprime:
 - ENCONTRADO + subconjunto (centavos e R$)
 - NÃO ENCONTRADO

Formato do CSV (compatível com o seu gerador):
name,pool,target
custom_30000,"[1,2,3,4,5,...]",735845023
"""

import sys
import os
import csv
import ast
from typing import List, Tuple

# ---------------- Utilidades ----------------

def fmt_centavos(x: int) -> str:
    s = f"{x/100:.2f}"
    return "R$ " + s.replace(".", ",")

def parse_pool_field(field: str) -> List[int]:
    s = field.strip()
    try:
        if s.startswith("[") and s.endswith("]"):
            lst = ast.literal_eval(s)
            return [int(x) for x in lst]
    except Exception:
        pass
    sep = ";" if ";" in s else ","
    parts = [p.strip() for p in s.split(sep) if p.strip()]
    return [int(p) for p in parts]

# ------------- DP bitset + reconstrução -------------

def bitset_dp_with_reconstruction(pool: List[int], T: int) -> Tuple[bool, List[int]]:
    n = len(pool)
    layers: List[int] = []
    dp = 1  # bit 0 ligado (soma 0)
    layers.append(dp)
    for v in pool:
        if v <= T:
            dp |= (dp << v)
        layers.append(dp)
    if ((dp >> T) & 1) == 0:
        return False, []
    subset: List[int] = []
    curT = T
    for i in range(n, 0, -1):
        v = pool[i-1]
        prev = layers[i-1]
        if ((prev >> curT) & 1) == 1:
            continue
        if curT >= v and ((prev >> (curT - v)) & 1) == 1:
            subset.append(v)
            curT -= v
    subset.reverse()
    return True, subset

# ---------------- Execução de 1 instância ----------------

def run_instance(name: str, pool: List[int], target: int) -> None:
    print("=" * 80)
    print(f"Instância: {name}")
    print(f"Alvo  : {target} -> {fmt_centavos(target)}")
    print(f"Itens : {len(pool)} valores")
    ok, subset = bitset_dp_with_reconstruction(pool, target)
    if ok:
        subtotal = sum(subset)
        print("\n>>> ENCONTRADO")
        print(f"Soma do subconjunto: {subtotal} -> {fmt_centavos(subtotal)}")
        print("Subconjunto (centavos):", subset)
        print("Subconjunto (R$)      :", [fmt_centavos(v) for v in subset])
    else:
        print("\n>>> NÃO ENCONTRADO")

# ---------------- Main (aceita argumento OU pergunta) ----------------

def main():
    # 1) Pega caminho do CSV: argumento ou prompt
    if len(sys.argv) >= 2:
        csv_path = sys.argv[1]
    else:
        print("Informe o caminho COMPLETO do CSV gerado (ex.: C:/Users/voce/Documentos/transacoes.csv)")
        csv_path = input("Caminho do CSV: ").strip().strip('"').strip("'")

    # 2) Valida existência; se não existir, pergunta novamente
    while not csv_path or not os.path.exists(csv_path):
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        csv_path = input("Caminho do CSV: ").strip().strip('"').strip("'")

    # 3) Lê e processa
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"name", "pool", "target"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            print("Erro: o CSV deve ter cabeçalho com colunas: name,pool,target")
            sys.exit(1)

        for i, row in enumerate(reader, start=2):
            try:
                name = row["name"]
                pool = parse_pool_field(row["pool"])
                target = int(row["target"].strip())
            except Exception as exc:
                print(f"[Linha {i}] erro ao parsear: {exc}")
                continue
            if target < 0 or any(v < 0 for v in pool):
                print(f"[{name}] Ignorada: valores/target negativos não são suportados.")
                continue
            run_instance(name, pool, target)

if __name__ == "__main__":
    main()
