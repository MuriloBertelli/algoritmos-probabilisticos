from typing import List, Tuple

# Matriz 2x3 do enunciado: 
JOGO_ENTRADA: List[List[Tuple[int, int]]] = [
    [(2, 1), (1, 0), (1, 0)],   # L1: Investe
    [(2, 1), (0, -1), (-1, 2)]  # L2: Não investe
]


def encontrar_nash(matriz: List[List[Tuple[float, float]]]) -> List[Tuple[int, int]]:
    
    if not matriz or not matriz[0]:
        return []

    m = len(matriz)       # nº de linhas 
    n = len(matriz[0])    # nº de colunas 

    
    max_dom_por_col = []
    for j in range(n):
        max_dom = max(matriz[i][j][0] for i in range(m))
        max_dom_por_col.append(max_dom)

    
    max_ent_por_lin = []
    for i in range(m):
        max_ent = max(matriz[i][j][1] for j in range(n))
        max_ent_por_lin.append(max_ent)

   
    eneps = []
    for i in range(m):
        for j in range(n):
            rD, rE = matriz[i][j]
            if rD >= max_dom_por_col[j] and rE >= max_ent_por_lin[i]:
                eneps.append((i, j))

    return eneps


def main() -> None:
    print("Jogo: Prevenção de Entrada (2x3)")
    eneps = encontrar_nash(JOGO_ENTRADA)
    print(f"O Equilíbrio de Nash em Estratégias Puras (ENEP) é encontrado nas coordenadas (Linha, Coluna): {eneps}")


if __name__ == "__main__":
    main()
