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
        ("Boca Raton", 8000),
    ],
    "Boca Raton": []
}

MAX_ALCANCE = 5000
MAX_PARADAS = 7
MAX_CUSTO = 15000

def buscar_rota_las_vegas(origem, destino, grafo=GRAFO,
                          max_paradas=MAX_PARADAS,
                          max_custo=MAX_CUSTO,
                          max_alcance=MAX_ALCANCE,
                          seed=None):
    if seed is not None:
        random.seed(seed)

    while True:
        atual = origem
        caminho = [atual]
        custo_total = 0
        paradas = 0

        while True:
            if atual == destino:
                if paradas <= max_paradas and custo_total <= max_custo:
                    return caminho, custo_total, paradas
                else:
                    break

            vizinhos_validos = []
            for proximo, custo in grafo.get(atual, []):
                if custo <= max_alcance:
                    vizinhos_validos.append((proximo, custo))

            if not vizinhos_validos:
                break

            proximo, custo = random.choice(vizinhos_validos)

            caminho.append(proximo)
            custo_total += custo
            paradas += 1
            atual = proximo

            if paradas > max_paradas or custo_total > max_custo:
                break


def main():
    origem = "Quatro Barras"
    destino = "Boca Raton"

    caminho, custo, paradas = buscar_rota_las_vegas(origem, destino)

    print("Rota encontrada (Las Vegas):")
    print(" -> ".join(caminho))
    print(f"Paradas: {paradas}")
    print(f"Custo total: {custo:.0f}")


if __name__ == "__main__":
    main()
