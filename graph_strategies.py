import importlib
import inspect
import pkgutil
from pathlib import Path
import csv
from typing import List

import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import numpy as np

fixed = ['C', 'D', 'D', 'D', 'C', 'C', 'C', 'C', 'D', 'C',
         'D', 'D', 'C', 'C', 'C', 'D', 'C', 'C', 'D', 'C']

POINTS = {
    ('C', 'C'): (3, 3),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (1, 1)
}

def load_strategies(package_name="strategies"):
    strategies = []
    package = importlib.import_module(package_name)
    package_path = Path(package.__file__).parent

    for _, mod_name, _ in pkgutil.iter_modules([str(package_path)]):
        module = importlib.import_module(f"{package_name}.{mod_name}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # only include classes defined in that file
            if obj.__module__ == module.__name__:
                # skip the abstract base class
                if name.lower() == "strategy":
                    continue
                strategies.append(obj)

    return strategies


def safe_move(player):
    """Call player.move() but protect against first-round IndexError bugs."""
    try:
        return player.move()
    except IndexError:
        return 'C'  # safe default if a strategy incorrectly assumes history exists


def play_round_fixed(p1, idx, sequence: List[str]):
    """
    Play one round versus a non-adapting fixed-sequence opponent.

    p1 : strategy instance
    idx: 0-based round index
    sequence: list of 'C'/'D' chars (fixed opponent script)
    Returns: (r1, r2, move1, move2)
    """
    move1 = safe_move(p1)
    move2 = sequence[idx] if idx < len(sequence) else sequence[-1]

    if move1 not in ("C", "D") or move2 not in ("C", "D"):
        raise ValueError(
            f"Invalid move: {p1.__class__.__name__} -> {move1}, Fixed -> {move2}"
        )

    r1, r2 = POINTS[(move1, move2)]

    # Update p1's internal state/history
    p1.record_result(move1, move2)

    return r1, r2, move1, move2


def play_game_vs_fixed(p1, sequence: List[str]):
    """
    Play p1 against the fixed script for len(sequence) rounds.

    Returns:
        total1, total2,
        moves1 (list[str]), moves2 (list[str]),
        rows (list[dict])  # round-by-round details
    """
    rounds = len(sequence)

    if hasattr(p1, "total_rounds"):
        p1.total_rounds = rounds

    total1 = total2 = 0
    moves1, moves2 = [], []
    rows = []

    for i in range(rounds):
        r1, r2, m1, m2 = play_round_fixed(p1, i, sequence)
        total1 += r1
        total2 += r2
        moves1.append(m1)
        moves2.append(m2)
        rows.append({
            "Round": i + 1,
            "StrategyMove": m1,
            "FixedMove": m2,
            "RoundScore_Strategy": r1,
            "RoundScore_Fixed": r2,
            "Cumulative_Strategy": total1,
            "Cumulative_Fixed": total2,
        })

    return total1, total2, moves1, moves2, rows

def save_round_by_round_plot(strategy_name: str, strat_moves: List[str], fixed_moves: List[str], out_png: Path):
    rounds = len(strat_moves)

    fig, ax = plt.subplots(figsize=(max(8, rounds * 0.25), 2.6))

    # y positions for rows (top row = strategy, bottom row = fixed)
    y_positions = [0, 1]

    # Draw dotted grid (optional)
    for r in y_positions:
        for c in range(rounds):
            ax.plot(c + 0.5, r + 0.5, marker='o',
                    markersize=18, fillstyle='none',
                    linestyle=':', color='gray', alpha=0.2)

    # Place dots
    for i, m in enumerate(strat_moves):
        ax.scatter(i + 0.5, 0 + 0.5,
                   s=200,
                   c='green' if m == 'C' else 'red')

    for i, m in enumerate(fixed_moves):
        ax.scatter(i + 0.5, 1 + 0.5,
                   s=200,
                   c='green' if m == 'C' else 'red')

    # Axis formatting
    ax.set_xlim(0, rounds)
    ax.set_ylim(0, 2)

    ax.set_xticks(range(rounds))
    ax.set_xticklabels(range(1, rounds + 1))
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels([strategy_name, "Fixed"])

    ax.invert_yaxis()
    ax.set_aspect("equal")

    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()


def run_fixed(sequence: List[str], save=True, make_plot=True):
    rounds = len(sequence)

    strategies = load_strategies()
    results = {}  # name -> score vs fixed
    match_rows = []

    print(f"loaded {len(strategies)} strategies:")
    for s in strategies:
        print("  -", s.__name__)
    print(f"Fixed opponent sequence ({rounds} rounds): {''.join(sequence)}")

    outdir = Path("graphs")
    outdir.mkdir(exist_ok=True)

    for S in strategies:
        p1 = S()
        score1, score2, moves1, moves2, rows = play_game_vs_fixed(p1, sequence)
        results[S.__name__] = score1
        print(f"{S.__name__} vs Fixed: {score1}-{score2}")

        # Save per-strategy round-by-round plot
        if make_plot:
            per_strategy_png = outdir / f"fixed_rounds_{rounds}_{S.__name__}.png"
            save_round_by_round_plot(S.__name__, moves1, moves2, per_strategy_png)


    # Print summary
    print("final rankings:")
    for name, total in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"{name:25s} {total}")


if __name__ == "__main__":
    run_fixed(fixed, save=True, make_plot=True)
