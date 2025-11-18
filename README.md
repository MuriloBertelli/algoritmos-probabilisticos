# algoritmos-probabilisticos

Assignments for the Probabilistic Algorithms course: Monte Carlo and Las Vegas methods, time series analysis (moving averages, AR models), lottery forecasting demos, stock price analysis, and Nash equilibrium search in game theory.

# Probabilistic Algorithms – Course Projects & Demos

---

## What is it made for?

Collection of study projects developed for a **Probabilistic Algorithms** course.

The repository brings theory to practice using:

* Monte Carlo and Las Vegas methods
* Random number generation and simulation
* Time series analysis (moving averages, autoregressive models)
* Financial data analysis with real stock prices (Petrobras)
* Lottery forecasting demos (Lotofácil and Mega-Sena)
* Game Theory and Nash Equilibrium in pure strategies

Each folder corresponds to a classroom assignment, implemented as a small, self-contained project.

---

## Structure

```
algoritmos-probabilisticos/
├── aulas/                        # Course slides (Aula 01–13)
├── petrobras_mms15/              # Time series analysis of Petrobras stock
│   ├── kkr.py                    # Main script (MMS(15) 2008–2015)
│   └── saidas_petrobras/         # Plots and CSV output
├── lotofacil_forecaster/         # Lotofácil forecasting demo
│   ├── lotofacil_forecaster.py   # Main script
│   ├── loto_facil_*.xlsx         # Historical draws (input data)
│   └── saida_lotofacil/          # Plots, CSV and suggestions
├── mega_sena_forecaster/         # Mega-Sena forecasting demo in C
│   ├── main.c                    # Main program
│   ├── mega_sena_*.csv/.xlsx     # Historical draws (input data)
│   └── megasena_forecaster.exe   # Optional compiled binary
├── nash_enep/                    # Nash Equilibrium in pure strategies
│   └── main.py                   # 2-player bi-matrix ENEP search
└── las_vegas_8_rainhas/          # Las Vegas algorithm for N-Queens
    └── main.py                   # Las Vegas + backtracking comparison
```

## Prerequisites

* **Python 3.10+** (for the Python projects)
* **GCC or another C compiler** (for the Mega-Sena project, if you want to build from source)

Required Python packages (for all Python projects):

```bash
pip install numpy pandas matplotlib statsmodels yfinance
```

Some input datasets (spreadsheets/CSVs) may be partially truncated to avoid versioning sensitive or heavy files.

## How to Use

### Clone the repository

```bash
git clone https://github.com/<your-user>/algoritmos-probabilisticos.git
cd algoritmos-probabilisticos
```

---

## Run each project

---

### Petrobras time series (MMS15)

```bash
cd petrobras_mms15
python kkr.py
```

### Lotofácil forecaster

```bash
cd lotofacil_forecaster
python lotofacil_forecaster.py \
  --xlsx loto_facil_asloterias_ate_concurso_3199_sorteio.xlsx
```

### Mega-Sena forecaster (C)

```bash
cd mega_sena_forecaster
gcc -O2 -o megasena_forecaster main.c -lm
./megasena_forecaster --csv mega_sena_asloterias_ate_concurso_2776_sorteio.csv
```

### Nash Equilibrium in Pure Strategies (ENEP)

```bash
cd nash_enep
python main.py
```

### Las Vegas – N Queens

```bash
cd las_vegas_8_rainhas
python main.py --n 8 --lv_runs 1000
```

---

# Logic Behind the Projects

### Stock time series (Petrobras – MMS15)

Uses daily prices of Petrobras stock from 2008–2015 to build a time series and compute a 15-day Simple Moving Average (SMA).
Illustrates trend detection, noise smoothing, and the basic idea of using moving averages for financial analysis.

---

### Lottery forecasters (Lotofácil & Mega-Sena)

---

For each lottery, the historical draws are transformed into binary time series (one series per number).
For every number, the scripts compute:

* historical frequency
* recent trend via moving average
* a simple AR(1) autoregressive forecast

These components are combined into a heuristic score to generate suggested games and visualizations.
The goal is to practice probabilistic and time-series tools, not to “beat” the lottery.

---

### Nash Equilibrium in Pure Strategies (Game Theory)

---

The ENEP script takes a bi-matrix game and finds cells where:

* the payoff of the row player is maximal in that column; and
* the payoff of the column player is maximal in that row.

These cells are pure-strategy Nash equilibria, matching the theoretical definition from the course.

---

### Las Vegas algorithm for N Queens

Compares:

* a Las Vegas algorithm that keeps sampling random board configurations until it finds a valid solution;
* a deterministic backtracking solver.

This shows the difference between Monte Carlo and Las Vegas algorithms in terms of correctness vs. runtime randomness.

---

# algoritmos-probabilisticos — Versão em Português

## Para que serve?

Coletânea de projetos desenvolvidos para a disciplina de **Algoritmos Probabilísticos**.

Este repositório aplica teoria à prática usando:

* Métodos de Monte Carlo e Las Vegas
* Geração de números aleatórios e simulação
* Análise de séries temporais (médias móveis, modelos autorregressivos)
* Análise de preços reais de ações (Petrobras)
* Previsão de loteria (Lotofácil e Mega-Sena)
* Teoria dos jogos e busca de Equilíbrio de Nash em estratégias puras

Cada pasta representa um exercício de aula, estruturado como um projeto autônomo.

## Estrutura

```
algoritmos-probabilisticos/
├── aulas/                        # Slides da disciplina (Aula 01–13)
├── petrobras_mms15/              # Análise temporal da Petrobras
│   ├── kkr.py                    # Script principal (MMS(15) 2008–2015)
│   └── saidas_petrobras/         # Gráficos e saídas CSV
├── lotofacil_forecaster/         # Previsor da Lotofácil
│   ├── lotofacil_forecaster.py   # Script principal
│   ├── loto_facil_*.xlsx         # Resultados históricos (entrada)
│   └── saida_lotofacil/          # Gráficos, CSVs e sugestões
├── mega_sena_forecaster/         # Previsor da Mega-Sena em C
│   ├── main.c                    # Programa principal
│   ├── mega_sena_*.csv/.xlsx     # Resultados históricos (entrada)
│   └── megasena_forecaster.exe   # Executável opcional
├── nash_enep/                    # Equilíbrio de Nash (estratégias puras)
│   └── main.py                   # Busca ENEP 2 jogadores
└── las_vegas_8_rainhas/          # Algoritmo Las Vegas para N-Rainhas
    └── main.py                   # Comparação LV + backtracking
```

## Pré-requisitos

* **Python 3.10+** (para os projetos em Python)
* **GCC ou outro compilador C** (para o projeto da Mega-Sena, se quiser compilar)

Pacotes Python necessários:

```bash
pip install numpy pandas matplotlib statsmodels yfinance
```

Alguns arquivos de entrada podem estar incompletos para evitar o versionamento de dados sensíveis ou pesados.

## Como usar

### Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/algoritmos-probabilisticos.git
cd algoritmos-probabilisticos
```

---

## Rodar cada projeto

---

### Série temporal Petrobras (MMS15)

```bash
cd petrobras_mms15
python kkr.py
```

### Previsor da Lotofácil

```bash
cd lotofacil_forecaster
python lotofacil_forecaster.py \
  --xlsx loto_facil_asloterias_ate_concurso_3199_sorteio.xlsx
```

### Previsor da Mega-Sena (C)

```bash
cd mega_sena_forecaster
gcc -O2 -o megasena_forecaster main.c -lm
./megasena_forecaster --csv mega_sena_asloterias_ate_concurso_2776_sorteio.csv
```

### Equilíbrio de Nash em Estratégias Puras (ENEP)

```bash
cd nash_enep
python main.py
```

### Las Vegas – 8 Rainhas

```bash
cd las_vegas_8_rainhas
python main.py --n 8 --lv_runs 1000
```

---

# Lógica dos Projetos

### Séries temporais (Petrobras – MMS15)

Usa preços diários da Petrobras de 2008–2015 para construir uma série temporal e calcular Média Móvel Simples (MMS15).
Mostra como detectar tendências, suavizar ruído e aplicar isso na análise financeira.

---

### Previsores de Loteria (Lotofácil & Mega-Sena)

Cada número vira uma série temporal binária com base nos sorteios históricos.
Para cada número são calculados:

* frequência histórica
* tendência recente via média móvel
* previsão AR(1) autorregressiva simples

Combina-se tudo em uma heurística para sugerir jogos e gerar visualizações.
O objetivo é exercitar estatística, não prever a sorte.

---

### Equilíbrio de Nash em Estratégias Puras

Recebe uma matriz de pagamentos e busca células onde:

* o jogador da linha tem o maior payoff naquela coluna; e
* o jogador da coluna tem o maior payoff naquela linha.

Essas células representam equilíbrios puros conforme a teoria dos jogos.

---

### Algoritmo Las Vegas – N Rainhas

Compara:

* algoritmo Las Vegas que tenta várias configurações aleatórias até achar uma solução válida;
* algoritmo determinístico com backtracking.

Ilustra a diferença entre Monte Carlo (probabilidade de acerto) e Las Vegas (tempo aleatório, mas resposta garantida).
