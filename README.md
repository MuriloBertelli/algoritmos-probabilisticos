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
