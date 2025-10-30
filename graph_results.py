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
TITLE = "Tournament Scores by Strategy"

def extract_round_number(filename: str) -> int:
    """
    Try to pull a tournament round number from a filename.
    Works with names like: results_round_12.txt, tournament_12.csv, foo-bar-12.log, etc.
    Falls back to the last number found if multiple are present.
    """
    # try round_###
    m = re.search(r"[Rr]ound[_\-]?(\d+)", filename)
    if m:
        return int(m.group(1))
    # otherwise use the last number in the filename
    nums = re.findall(r"\d+", filename)
    if nums:
        return int(nums[-1])
    # if no number at all, use -1 so it sorts first (or gets ignored)
    return -1

def parse_final_score_line(line: str):
    """
    Parse a line like:
        'final score,DefectTitForTat,7173,'  OR  'final score, MiniMax , 4596'
    Returns (strategy_name, score) or None if not a final score line.
    """
    if not line.lower().startswith("final score"):
        return None

    # split and strip empty trailing parts
    parts = [p.strip() for p in line.strip().split(",") if p.strip() != ""]
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
            # skip files with no round id
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
    Plot one line per strategy with distinct colors.
    Missing data for a round becomes NaN so lines break rather than connect incorrectly.
    """
    import numpy as np
    import itertools
    import matplotlib.cm as cm

    plt.figure(figsize=(10, 6))

    # use a colormap to assign distinct colors
    n = len(scores)
    color_map = matplotlib.colormaps["nipy_spectral"]
    colors = itertools.cycle(color_map(np.linspace(0, 1, n)))

    for strat, by_round in scores.items():
        y = [by_round.get(r, math.nan) for r in rounds_sorted]
        plt.plot(rounds_sorted, y, label=strat, color=next(colors), linewidth=1.8)

    plt.xlabel("Tournament Round")
    plt.ylabel("Final Score")
    plt.title(title)

    # legend placement
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.,
                   fontsize="small", ncol=2)

    plt.grid(True, which="both", linestyle="--", alpha=0.3)
    plt.tight_layout()

    os.makedirs("graphs", exist_ok=True)
    plt.savefig("graphs/plot.png", bbox_inches="tight", dpi=200)
    plt.close()



if __name__ == "__main__":
    rounds_sorted, scores = load_scores_by_round(DIRECTORY)

    if not rounds_sorted or not scores:
        raise SystemExit("No rounds or scores found. Check DIRECTORY and file contents.")

    filtered_scores = select_top_k(scores, rounds_sorted, TOP_K)
    plot_scores(rounds_sorted, filtered_scores, TITLE)

