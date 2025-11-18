# n_queens_las_vegas.py
import random
import time
import argparse
from typing import List, Optional, Tuple

# ---------- util ----------
def is_valid(cols: List[int]) -> bool:
    
    n = len(cols)
    rows = set(cols)
    if len(rows) != n:  # duas na mesma linha
        return False
    diag1 = set()  
    diag2 = set()  
    for c, r in enumerate(cols):
        d1 = r - c
        d2 = r + c
        if d1 in diag1 or d2 in diag2:
            return False
        diag1.add(d1); diag2.add(d2)
    return True

def pretty_board(cols: List[int]) -> str:
    n = len(cols)
    rows = []
    for r in range(n):
        line = ["·"] * n
        for c, rr in enumerate(cols):
            if rr == r:
                line[c] = "Q"
        rows.append(" ".join(line))
    return "\n".join(rows)

# ---------- Las Vegas ----------
def las_vegas_once(n: int, rng: random.Random) -> Tuple[List[int], int]:
    
    attempts = 0
    while True:
        attempts += 1
        cols = [rng.randrange(n) for _ in range(n)]
        if is_valid(cols):
            return cols, attempts

def las_vegas_stats(n: int, runs: int, seed: int = 42):
    rng = random.Random(seed)
    t0 = time.perf_counter()
    attempts_list = []
    last_solution = None
    for _ in range(runs):
        sol, att = las_vegas_once(n, rng)
        attempts_list.append(att)
        last_solution = sol
    t1 = time.perf_counter()
    return {
        "n": n,
        "runs": runs,
        "avg_attempts": sum(attempts_list) / runs,
        "max_attempts": max(attempts_list),
        "min_attempts": min(attempts_list),
        "total_time_s": t1 - t0,
        "last_solution": last_solution,
    }

# ---------- Backtracking  ----------
def backtrack_solve(n: int) -> Tuple[List[int], int]:
    
    cols = [-1] * n
    rows_used = set()
    d1_used = set()  # r-c
    d2_used = set()  # r+c
    nodes = 0

    def dfs(c: int) -> bool:
        nonlocal nodes
        nodes += 1
        if c == n:
            return True
        for r in range(n):
            d1 = r - c
            d2 = r + c
            if r in rows_used or d1 in d1_used or d2 in d2_used:
                continue
            cols[c] = r
            rows_used.add(r); d1_used.add(d1); d2_used.add(d2)
            if dfs(c + 1):
                return True
            rows_used.remove(r); d1_used.remove(d1); d2_used.remove(d2)
            cols[c] = -1
        return False

    dfs(0)
    return cols, nodes

def backtracking_benchmark(n: int, runs: int = 3):
    total_time = 0.0
    last_solution = None
    last_nodes = 0
    for _ in range(runs):
        t0 = time.perf_counter()
        sol, nodes = backtrack_solve(n)
        total_time += time.perf_counter() - t0
        last_solution = sol
        last_nodes = nodes
    return {
        "n": n,
        "runs": runs,
        "avg_time_s": total_time / runs,
        "last_solution": last_solution,
        "last_nodes": last_nodes,
    }


def main():
    # para roda o codigo, python main.py --n 8 --lv_runs 5000 --bt_runs 3
    # para roda 2; codigo, python mian.py --n 10 --lv_runs 10000 --bt_runs 5 
    # if (seed == default): seed = 42
    ap = argparse.ArgumentParser(
        description="N-Queens — Las Vegas vs Backtracking"
    )
    ap.add_argument("--n", type=int, default=8, help="tamanho do tabuleiro (N)")
    ap.add_argument("--lv_runs", type=int, default=1000,
                    help="quantas rodadas para estatística do Las Vegas")
    ap.add_argument("--seed", type=int, default=42, help="seed do RNG")
    ap.add_argument("--bt_runs", type=int, default=3,
                    help="quantas vezes cronometrar o backtracking")
    args = ap.parse_args()

    # Las Vegas
    lv = las_vegas_stats(args.n, args.lv_runs, seed=args.seed)
    print("\n=== Las Vegas ===")
    print(f"N={args.n} | rodadas={args.lv_runs}")
    print(f"Média de tentativas: {lv['avg_attempts']:.2f} "
          f"(min={lv['min_attempts']}, max={lv['max_attempts']})")
    print(f"Tempo total: {lv['total_time_s']:.4f}s "
          f"(~{lv['total_time_s']/args.lv_runs:.6f}s/solução)")
    print("Solução (última):", lv["last_solution"])
    print(pretty_board(lv["last_solution"]))

    # Backtracking
    bt = backtracking_benchmark(args.n, runs=args.bt_runs)
    print("\n=== Backtracking ===")
    print(f"N={args.n} | runs={args.bt_runs}")
    print(f"Tempo médio: {bt['avg_time_s']:.6f}s")
    print(f"Nós explorados (última): {bt['last_nodes']}")
    print("Solução (última):", bt["last_solution"])
    print(pretty_board(bt["last_solution"]))

   
if __name__ == "__main__":
    main()
