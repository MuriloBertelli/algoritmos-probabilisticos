import random

GRAFO = {
    "Quatro Barras": [
        ("Curitiba", 500),
        ("Joinville", 1400),
        ("Ponta Grossa", 1600),
    ],
    "Curitiba": [
        ("São Paulo", 4000),
        ("Londrina", 4200),
        ("Joinville", 3000),
    ],
    "Joinville": [
        ("Curitiba", 3000),
        ("Florianópolis", 3500),
    ],
    "Ponta Grossa": [
        ("Curitiba", 2000),
        ("Londrina", 4500),
    ],
    "São Paulo": [
        ("Campinas", 800),
        ("Rio de Janeiro", 3200),
    ],
    "Londrina": [
        ("Maringá", 1200),
        ("São Paulo", 3800),
    ],
    "Florianópolis": [
        ("Porto Alegre", 4500),
    ],
    "Campinas": [
        ("Rio de Janeiro", 2500),
    ],
    "Maringá": [
        ("São Paulo", 4200),
    ],
    "Porto Alegre": [
        ("Curitiba", 4800),
        ("Rio de Janeiro", 7000),
    ],
    "Rio de Janeiro": [
        ("Boca Raton", 5000),
    ],
    "Boca Raton": []
}

MAX_ALCANCE = 5000
MAX_PARADAS = 7
MAX_CUSTO = 15000

def buscar_rota_las_vegas(origem, destino, max_tentativas=100000):
    tentativas = 0

    while True:
        tentativas += 1
        if tentativas % 1000 == 0:
            print(f"Tentativa #{tentativas}...")

        atual = origem
        caminho = [atual]
        custo_total = 0
        paradas = 0

        while True:
            vizinhos = GRAFO.get(atual, [])

            
            vizinhos_validos = [(v, c) for (v, c) in vizinhos if c <= 5000]

            if not vizinhos_validos:
               
                break

            prox, custo = random.choice(vizinhos_validos)
            caminho.append(prox)
            custo_total += custo
            paradas += 1
            atual = prox

            if atual == destino:
                
                if paradas < 7 and custo_total < 15000:
                    print(f"Achou solução na tentativa #{tentativas}")
                    return caminho, custo_total, paradas
                else:
                    
                    break

            
            if paradas >= 7 or custo_total >= 15000:
                break

        if tentativas >= max_tentativas:
            print(f"Nenhuma rota encontrada em {max_tentativas} tentativas.")
            return None, None, None
## =========TESTES==========#

# def todas_rotas_validas(grafo, origem, destino,
#                         max_paradas=6, max_custo=15000):
#     resultados = []

#     def dfs(atual, custo, caminho):
#         if len(caminho) - 1 > max_paradas:
#             return
#         if custo > max_custo:
#             return

#         if atual == destino:
#             resultados.append((list(caminho), custo))
#             return

#         for prox, dist in grafo[atual]:
#             if prox in caminho:
#                 continue
#             dfs(prox, custo + dist, caminho + [prox])

#     dfs(origem, 0, [origem])
#     return resultados
## =========T==========#

def main():
    origem = "Quatro Barras"
    destino = "Boca Raton"

    caminho, custo, paradas = buscar_rota_las_vegas(origem, destino)

    if caminho is None:
        print("Nenhuma rota que satisfaça as restrições foi encontrada.")
    else:
        print("Rota encontrada:")
        print(" -> ".join(caminho))
        print(f"Custo total: {custo}")
        print(f"Paradas: {paradas}")
    ## =========TESTES==========#
    # rotas = todas_rotas_validas(GRAFO, origem, destino,
    #                         max_paradas=6, max_custo=15000)

    # print(f"Qtde de rotas válidas determinísticas: {len(rotas)}")
    # for cam, custo in rotas[:10]:
    #     print("Rota:", " -> ".join(cam), "| custo:", custo)
    ## =========T==========#

if __name__ == "__main__":
    main()

