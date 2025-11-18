# petrobras_mms15.py
# Série PETROBRAS 2008-2015, MMS(15) por ano e no geral, com retries e fallback.

import argparse
import os
from pathlib import Path
import time

import pandas as pd
import matplotlib.pyplot as plt

try:
    import yfinance as yf
except Exception:
    yf = None



def to_scalar(x) -> float:
    
    if hasattr(x, "to_numpy"):
        arr = x.to_numpy()
        return float(arr[0]) if arr.ndim == 1 else float(arr.squeeze()[()])
    return float(x)



def load_from_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    
    close_col = None
    for cand in ["Close", "close", "Adj Close", "Adj_Close", "adj_close", "AdjClose"]:
        if cand in df.columns:
            close_col = cand
            break
    if close_col is None:
        raise RuntimeError("CSV não tem coluna de preço ('Close' / 'Adj Close').")

    
    if "Date" in df.columns:
        idx = pd.to_datetime(df["Date"])
    elif "date" in df.columns:
        idx = pd.to_datetime(df["date"])
    else:
        raise RuntimeError("CSV não tem coluna de data ('Date').")

    out = pd.DataFrame({"close": df[close_col].astype(float).values}, index=idx)
    out = out.dropna()
    out.index = pd.to_datetime(out.index)
    out["year"] = out.index.year
    return out


def download_prices_yf(ticker: str, start="2008-01-01", end="2015-12-31",
                       retries: int = 3, sleep_sec: float = 2.0) -> pd.DataFrame:
    if yf is None:
        raise RuntimeError("Pacote yfinance não disponível. Instale com: pip install yfinance")

    last_exc = None
    for i in range(retries):
        try:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                auto_adjust=True,
                progress=False,
                threads=False,   
                interval="1d",
                timeout=30,
            )
            if not df.empty:
                df = df[["Close"]].rename(columns={"Close": "close"}).dropna()
                df.index = pd.to_datetime(df.index)
                df["year"] = df.index.year
                return df
        except Exception as e:
            last_exc = e
        time.sleep(sleep_sec)

    raise RuntimeError(f"Falha ao baixar {ticker}: {last_exc}")


def get_prices(ticker: str, csv_path: str | None) -> pd.DataFrame:
    if csv_path:
        print(f"Lendo dados do CSV: {csv_path}")
        return load_from_csv(csv_path)
    print(f"Baixando {ticker} (2008–2015)...")
    try:
        return download_prices_yf(ticker)
    except RuntimeError as e:
        # tenta fallback de ticker (PETR3 <-> PETR4)
        alt = "PETR3.SA" if ticker.upper().startswith("PETR4") else "PETR4.SA"
        print(f"Aviso: {e}\nTentando fallback {alt} ...")
        return download_prices_yf(alt)



def plot_year(df_year: pd.DataFrame, year: int, outdir: Path):
    s = df_year["close"]
    mms15 = s.rolling(window=15, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
    ax.plot(s.index, s.values, label="Fechamento", linewidth=1.1)
    ax.plot(mms15.index, mms15.values, label="MMS 15 dias", linewidth=1.6)
    ax.set_title(f"{year} — {len(df_year)} pregões")
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (R$)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    out = outdir / f"petrobras_{year}_MMS15.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def plot_overall(df: pd.DataFrame, outdir: Path, title: str):
    s = df["close"]
    mms15 = s.rolling(window=15, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(12, 6), dpi=120)
    ax.plot(s.index, s.values, label="Fechamento", linewidth=0.9)
    ax.plot(mms15.index, mms15.values, label="MMS 15 dias", linewidth=1.6)
    ax.set_title(f"{title} — 2008–2015 (MMS 15 dias)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (R$)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    out = outdir / "petrobras_2008_2015_MMS15.png"
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out



def analyze_trend(df: pd.DataFrame):
    
    rows = []
    for year, chunk in df.groupby("year"):
        first = to_scalar(chunk["close"].iloc[0])     
        last = to_scalar(chunk["close"].iloc[-1])     
        delta = round(last - first, 2)
        up = (last > first)                           
        rows.append({
            "ano": year,
            "primeiro_dia": round(first, 2),
            "ultimo_dia": round(last, 2),
            "Δ(R$)": delta,
            "Δ(%)": round(100 * (last / first - 1), 2) if first != 0 else None,
            "subiu?": "SIM" if up else "NÃO",
        })

    out = pd.DataFrame(rows).sort_values("ano").reset_index(drop=True)

    first_all = to_scalar(df["close"].iloc[0])
    last_all  = to_scalar(df["close"].iloc[-1])
    overall_up = "SIM" if (last_all > first_all) else "NÃO"
    return out, round(first_all, 2), round(last_all, 2), overall_up



def main():
    parser = argparse.ArgumentParser(description="Média Móvel Petrobras 2008–2015")
    parser.add_argument("--ticker", default="PETR4.SA", help="ex.: PETR4.SA ou PETR3.SA")
    parser.add_argument("--outdir", default="saidas_petrobras", help="pasta de saída")
    parser.add_argument("--csv", default=None, help="usar CSV local (contendo Date e Close)")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    df = get_prices(args.ticker, args.csv)

    print("Gerando gráficos anuais (MMS 15 dias)...")
    for year, chunk in df.groupby("year"):
        p = plot_year(chunk, year, outdir)
        print(f"  - {year}: {p.name}")

    p_all = plot_overall(df, outdir, title=args.ticker if args.csv is None else "CSV local")
    print(f"Gráfico geral salvo em: {p_all}")

    tbl, first_all, last_all, overall_up = analyze_trend(df)
    print("\nResumo — 1º dia vs último dia do ANO:")
    print(tbl.to_string(index=False))
    print(f"\nPeríodo completo 2008–2015: primeiro={first_all:.2f} | último={last_all:.2f} "
          f"| subiu no geral? {overall_up}")

    df_out = df.copy()
    df_out["mms15"] = df_out["close"].rolling(15, min_periods=1).mean()
    csv_path = outdir / "petrobras_2008_2015_mms15.csv"
    df_out.to_csv(csv_path, index=True)
    print(f"\nCSV com preços e MMS salvo em: {csv_path}")


if __name__ == "__main__":
    main()
