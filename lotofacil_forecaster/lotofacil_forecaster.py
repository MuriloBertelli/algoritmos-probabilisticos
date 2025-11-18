import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


try:
    from statsmodels.tsa.ar_model import AutoReg
    HAVE_SM = True
except Exception:
    HAVE_SM = False



def read_draws_xlsx(path: str) -> pd.DataFrame:
    """
    Lê o XLSX da Lotofácil e retorna um DataFrame (n x 15) com as dezenas de cada concurso.
    Tenta (1) colunas que contenham 'bola'; (2) as 15 últimas colunas; (3) as colunas 2..16 (C..Q).
    Remove linhas não numéricas e garante inteiros entre 1..25.
    """
    df = pd.read_excel(path, engine="openpyxl")

    # (1) Procura colunas com 'bola' no título
    bola_cols = [c for c in df.columns if isinstance(c, str) and 'bola' in c.lower()]
    if len(bola_cols) >= 15:
        # Ordena pelas numerações, se possível (bola 1, bola 2, ...)
        def _key(c):
            import re
            m = re.search(r'(\d+)', str(c))
            return int(m.group(1)) if m else 999
        bola_cols = sorted(bola_cols, key=_key)[:15]
        draws = df[bola_cols].copy()
    else:
        # (2) Tenta as 15 últimas colunas (comum em planilhas "C..Q")
        draws = df.iloc[:, -15:].copy()
        # se ainda assim não estiver correto, tenta (3) C..Q explicitamente
        if draws.shape[1] < 15:
            draws = df.iloc[:, 2:17].copy()

    # Converte para numérico, ignora cabeçalhos no meio
    draws = draws.apply(pd.to_numeric, errors="coerce")
    # Mantém linhas onde TODAS as 15 colunas são 1..25
    mask_valid = draws.ge(1) & draws.le(25)
    draws = draws[mask_valid.all(axis=1)]

    draws = draws.dropna(how="any").astype(int).reset_index(drop=True)
    draws.columns = [f"bola_{i+1}" for i in range(15)]
    assert draws.shape[1] == 15 and len(draws) > 0, "Não consegui extrair 15 dezenas por concurso do XLSX."
    return draws


# ===================== INDICADOR 0/1 =====================
def to_indicator_matrix(draws: pd.DataFrame) -> pd.DataFrame:
    
    N = len(draws)
    mat = np.zeros((N, 25), dtype=int)
    for i, row in draws.iterrows():
        for v in row.values:
            if 1 <= v <= 25:
                mat[i, v - 1] = 1
    idx = pd.RangeIndex(start=1, stop=N + 1, step=1, name="concurso")
    cols = [f"d{j}" for j in range(1, 26)]
    return pd.DataFrame(mat, index=idx, columns=cols)



def moving_average_signal(ind: pd.DataFrame, window: int = 20) -> pd.Series:
    
    roll = ind.rolling(window=window, min_periods=1).mean()
    return roll.iloc[-1]


def ar1_signal(ind: pd.DataFrame) -> pd.Series:
    
    preds = []
    for c in ind.columns:
        y = ind[c].astype(float).values
        if HAVE_SM and len(y) >= 10 and np.any(y) and np.any(1 - y):
            try:
                model = AutoReg(y, lags=1, old_names=False)
                res = model.fit()
                p = res.predict(start=len(y), end=len(y))
                preds.append(float(p[0]))
                continue
            except Exception:
                pass
        
        alpha = 0.3
        ewma = pd.Series(y).ewm(alpha=alpha, adjust=False).mean().iloc[-1]
        preds.append(float(ewma))
    return pd.Series(preds, index=ind.columns)


def freq_signal(ind: pd.DataFrame) -> pd.Series:
    
    return ind.mean(axis=0)


def combine_scores(freq: pd.Series, ma: pd.Series, ar: pd.Series,
                   w_freq=0.3, w_ma=0.4, w_ar=0.3) -> pd.Series:
    
    return w_freq * freq + w_ma * ma + w_ar * ar


# ===================== PALPITES =====================
def make_ticket_from_scores(score: pd.Series, k=15) -> list[int]:
    """Seleciona as k dezenas com maior score."""
    order = score.sort_values(ascending=False)
    top = order.index[:k]
    return sorted([int(s[1:]) for s in top])  # d1..d25 -> 1..25


def diversify_tickets(base_score: pd.Series, n_extra=3, k=15,
                      jitter=0.05, seed=42) -> list[list[int]]:
    
    rng = np.random.default_rng(seed)
    tickets = []
    for _ in range(n_extra):
        noise = pd.Series(rng.normal(loc=0.0, scale=jitter, size=len(base_score)),
                          index=base_score.index)
        s = base_score + noise
        tickets.append(make_ticket_from_scores(s, k=k))
    return tickets



def plot_frequency(ind: pd.DataFrame, outdir: Path):
    freq = ind.mean(axis=0)
    xs = np.arange(1, 26)
    plt.figure(figsize=(10, 4), dpi=120)
    plt.bar(xs, freq.values, width=0.8)
    plt.xticks(xs)
    plt.title("Lotofácil — Frequência histórica por dezena")
    plt.xlabel("Dezena")
    plt.ylabel("Proporção de sorteios")
    out = outdir / "frequencia_historica.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def plot_trend(ind: pd.DataFrame, window=20, outdir: Path | None = None):
    
    freq = ind.mean(axis=0)
    top = freq.sort_values(ascending=False).index[:5]
    roll = ind[top].rolling(window=window, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(10, 4), dpi=120)  
    roll.plot(ax=ax)                                  
    ax.set_title(f"Média móvel ({window}) das dezenas mais frequentes")
    ax.set_xlabel("Concurso")
    ax.set_ylabel("Proporção")
    ax.legend([t.replace('d', 'dez ') for t in top], loc='best')

    out = None
    if outdir is not None:
        out = outdir / f"tendencia_mms{window}.png"
        fig.tight_layout()
        fig.savefig(out)
        plt.close(fig)
    else:
        plt.show()
    return out



def main():
    ap = argparse.ArgumentParser(
        description="Previsão heurística Lotofácil — frequência + média móvel + AR(1)"
    )
    ap.add_argument("--xlsx", required=True, help="Caminho do XLSX com os sorteios (15 dezenas por linha)")
    ap.add_argument("--window", type=int, default=20, help="Janela da média móvel (padrão=20)")
    ap.add_argument("--wf", type=float, default=0.30, help="Peso da frequência histórica")
    ap.add_argument("--wm", type=float, default=0.40, help="Peso da média móvel")
    ap.add_argument("--wa", type=float, default=0.30, help="Peso do autoregressivo")
    ap.add_argument("--extras", type=int, default=3, help="Qtde de jogos extra (diversificados)")
    ap.add_argument("--outdir", default="saida_lotofacil", help="Pasta de saída")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    
    draws = read_draws_xlsx(args.xlsx)
    ind = to_indicator_matrix(draws)

    
    freq = freq_signal(ind)
    ma = moving_average_signal(ind, window=args.window)
    ar = ar1_signal(ind)

    
    score = combine_scores(freq, ma, ar, w_freq=args.wf, w_ma=args.wm, w_ar=args.wa)

   
    principal = make_ticket_from_scores(score, k=15)
    extras = diversify_tickets(score, n_extra=args.extras, k=15)

    
    f1 = plot_frequency(ind, outdir)
    f2 = plot_trend(ind, window=args.window, outdir=outdir)

    
    print("\n=== Relatório — sinais por dezena (1..25) ===")
    table = pd.DataFrame({
        "dezena": [int(c[1:]) for c in score.index],
        "freq_hist": np.round(freq.values, 4),
        f"mms_{args.window}": np.round(ma.values, 4),
        "ar_score": np.round(ar.values, 4),
        "score_final": np.round(score.values, 5)
    }).sort_values("score_final", ascending=False).reset_index(drop=True)
    print(table.to_string(index=False))

    print("\nPalpite principal:", principal)
    for i, t in enumerate(extras, 1):
        print(f"Variação #{i}:", t)

    out_csv = outdir / "sinais_e_scores.csv"
    table.to_csv(out_csv, index=False)

    print(f"\nArquivos salvos em: {outdir}")
    print(f" - Frequência: {f1}")
    print(f" - Tendência:  {f2}")
    print(f" - Sinais CSV: {out_csv}")

    print("\n⚠️ Aviso didático: Loterias são essencialmente aleatórias; "
          "isso é uma heurística para estudo (freq + média móvel + AR), sem garantia de acerto.")


if __name__ == "__main__":
    main()
