# algoritmos-probabilisticos
Assignments for the Probabilistic Algorithms course: Monte Carlo and Las Vegas methods, time series analysis (moving averages, AR models), lottery forecasting demos, stock price analysis, and Nash equilibrium search in game theory.

# Probabilistic Algorithms – Course Projects & Demos

---

## What is it made for?

Collection of study projects developed for a **Probabilistic Algorithms** course.

The repository brings theory to practice using:

- Monte Carlo and Las Vegas methods  
- Random number generation and simulation  
- Time series analysis (moving averages, autoregressive models)  
- Financial data analysis with real stock prices (Petrobras)  
- Lottery forecasting demos (Lotofácil and Mega-Sena)  
- Game Theory and Nash Equilibrium in pure strategies  

Each folder corresponds to a classroom assignment, implemented as a small, self-contained project.

---

## Structure

```text
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
---

## Prerequisites

Python 3.10+ (for the Python projects)

GCC or another C compiler (for the Mega-Sena project, if you want to build from source)

Required Python packages (for all Python projects):

pip install numpy pandas matplotlib statsmodels yfinance


You can also create a requirements.txt with these libraries and run:

pip install -r requirements.txt


How to Use

Clone the repository

git clone https://github.com/<your-user>/algoritmos-probabilisticos.git
cd algoritmos-probabilisticos


(Optional) Create and activate a virtual environment

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate


Install the Python dependencies

pip install numpy pandas matplotlib statsmodels yfinance


Run each project

Petrobras time series (MMS15)

cd petrobras_mms15
python kkr.py


Lotofácil forecaster

cd lotofacil_forecaster
python lotofacil_forecaster.py \
  --xlsx loto_facil_asloterias_ate_concurso_3199_sorteio.xlsx


Mega-Sena forecaster (C)

cd mega_sena_forecaster
gcc -O2 -o megasena_forecaster main.c -lm
./megasena_forecaster --csv mega_sena_asloterias_ate_concurso_2776_sorteio.csv


Nash Equilibrium in Pure Strategies (ENEP)

cd nash_enep
python main.py


Las Vegas – N Queens

cd las_vegas_8_rainhas
python main.py --n 8 --lv_runs 1000

Logic Behind the Projects

Stock time series (Petrobras – MMS15)
Uses daily prices of Petrobras stock from 2008–2015 to build a time series and compute a 15-day Simple Moving Average.
This illustrates trend detection, noise smoothing and the basic idea of using moving averages for financial analysis.

Lottery forecasters (Lotofácil & Mega-Sena)
For each lottery, the historical draws are transformed into binary time series (one series per number).
For every number the scripts compute:

historical frequency;

recent trend via moving average;

a simple AR(1) autoregressive forecast.

These components are combined into a heuristic score to generate suggested games and visualizations.
The goal is to practice probabilistic and time-series tools, not to “beat” the lottery.

Nash Equilibrium in Pure Strategies (Game Theory)
The ENEP script takes a bi-matrix game and finds cells where:

the payoff of the row player is maximal in that column;

and the payoff of the column player is maximal in that row.

Such cells are pure-strategy Nash equilibria, matching the theoretical definition from the course.

Las Vegas algorithm for N Queens
Compares:

a Las Vegas algorithm that keeps sampling random board configurations until it finds a valid solution;

a deterministic backtracking solver.

This illustrates the difference between Monte Carlo and Las Vegas algorithms in terms of correctness vs. runtime randomness.

Important Note

Lottery data and stock price series are used for academic purposes only.

Forecasts and suggested games do not provide any guarantee of financial gain or lottery winnings.

Some input datasets (spreadsheets/CSVs) may be partially truncated to avoid versioning sensitive or heavy files.

Use this repository as a learning toolkit for probabilistic algorithms, experimentation and visualization.
