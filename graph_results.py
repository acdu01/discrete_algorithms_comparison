import os
import re
import math
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt

DIRECTORY = "tournament_results"   
TOP_K = None                        
TITLE = "Tournament Scores by Strategy (one line per strategy)"

def extract_round_number(filename: str) -> int:
    """
    Try to pull a tournament round number from a filename.
    Works with names like: results_round_12.txt, tournament_12.csv, foo-bar-12.log, etc.
    Falls back to the last number found if multiple are present.
    """
    # Prefer patterns like 'round_###'
    m = re.search(r"[Rr]ound[_\-]?(\d+)", filename)
    if m:
        return int(m.group(1))
    # Otherwise use the last number in the filename
    nums = re.findall(r"\d+", filename)
    if nums:
        return int(nums[-1])
    # If no number at all, use -1 so it sorts first (or gets ignored)
    return -1

def parse_final_score_line(line: str):
    """
    Parse a line like:
        'final score,DefectTitForTat,7173,'  OR  'final score, MiniMax , 4596'
    Returns (strategy_name, score) or None if not a final score line.
    """
    if not line.lower().startswith("final score"):
        return None

    # Split and strip empty trailing parts
    parts = [p.strip() for p in line.strip().split(",") if p.strip() != ""]
    # Expected: ["final score", "<StrategyName>", "<Score>"]
    if len(parts) < 3:
        return None

    strategy_name = parts[1]
    try:
        score = int(parts[2])
    except ValueError:
        return None
    return strategy_name, score

def load_scores_by_round(directory: str):
    """
    Reads every file in `directory`, collects final scores per round per strategy.

    Returns:
        rounds_sorted: list[int]  -> all discovered rounds sorted ascending
        scores: dict[strategy -> dict[round -> score]]
    """
    scores = defaultdict(dict)  # strategy -> { round -> score }
    rounds_seen = set()

    for fname in os.listdir(directory):
        fpath = os.path.join(directory, fname)
        if not os.path.isfile(fpath):
            continue

        rnd = extract_round_number(fname)
        if rnd < 0:
            # Skip files with no parseable round id
            continue

        rounds_seen.add(rnd)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parsed = parse_final_score_line(line)
                if parsed is None:
                    continue
                strategy, score = parsed
                scores[strategy][rnd] = score

    rounds_sorted = sorted(rounds_seen)
    return rounds_sorted, scores

def select_top_k(scores: dict, rounds_sorted: list[int], k: int):
    """
    Select top-k strategies by average score over available rounds.
    """
    if k is None:
        return scores  # no filtering

    avg_scores = []
    for strat, by_round in scores.items():
        vals = [by_round[r] for r in rounds_sorted if r in by_round]
        if not vals:
            continue
        avg_scores.append((strat, sum(vals) / len(vals)))
    avg_scores.sort(key=lambda x: x[1], reverse=True)
    keep = set([s for s, _ in avg_scores[:k]])

    return {s: by_round for s, by_round in scores.items() if s in keep}

def plot_scores(rounds_sorted, scores, title=TITLE):
    """
    Plot one line per strategy. Missing data for a round becomes NaN so lines break rather than connect incorrectly.
    """
    # Build aligned Y arrays per strategy
    import numpy as np
    for strat, by_round in scores.items():
        y = [by_round.get(r, math.nan) for r in rounds_sorted]
        plt.plot(rounds_sorted, y, label=strat)  # do not set colors; follow default style

    plt.xlabel("Tournament Round")
    plt.ylabel("Final Score")
    plt.title(title)
    # Put legend outside if many strategies
    n = len(scores)
    if n <= 12:
        plt.legend()
    else:
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", borderaxespad=0.)
        plt.tight_layout()

    plt.grid(True, which="both", linestyle="--", alpha=0.3)
    plt.savefig("graphs/plot.png")

if __name__ == "__main__":
    rounds_sorted, scores = load_scores_by_round(DIRECTORY)

    if not rounds_sorted or not scores:
        raise SystemExit("No rounds or scores found. Check DIRECTORY and file contents.")

    filtered_scores = select_top_k(scores, rounds_sorted, TOP_K)
    plot_scores(rounds_sorted, filtered_scores, TITLE)

