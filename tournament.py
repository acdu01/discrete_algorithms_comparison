import importlib
import inspect
import pkgutil
from pathlib import Path
import csv

POINTS = {
    ('C', 'C'): (3, 3),  # both cooperate
    ('C', 'D'): (0, 5),  # first cooperate, second betray
    ('D', 'C'): (5, 0),  # first betray, second cooperate
    ('D', 'D'): (1, 1)   # both betray
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




def play_round(p1, p2):
    # both players pick a move
    move1 = p1.move()
    move2 = p2.move()


    # look up their scores from the table
    r1, r2 = POINTS[(move1, move2)]


    # tell each player what happened
    p1.record_result(move1, move2)
    p2.record_result(move2, move1)


    return r1, r2


def play_game(p1, p2, rounds=100):
    # keep track of total points for both players
    total1 = total2 = 0
    for _ in range(rounds):
        r1, r2 = play_round(p1, p2)
        total1 += r1
        total2 += r2
    return total1, total2


def run_tournament(rounds=100, save=True):
    # grab all the strategies we found
    strategies = load_strategies()
    results = {s.__name__: 0 for s in strategies}
    match_data = []


    print(f"loaded {len(strategies)} strategies:")
    for s in strategies:
        print("  -", s.__name__)


    # everyone plays everyone else once
    for i, S1 in enumerate(strategies):
        for j, S2 in enumerate(strategies):
            if i >= j:
                continue  # skip repeats and playing against self
            p1 = S1()
            p2 = S2()
            score1, score2 = play_game(p1, p2, rounds)


            results[S1.__name__] += score1
            results[S2.__name__] += score2


            print(f"{S1.__name__} vs {S2.__name__}: {score1}-{score2}")


            match_data.append({
                "Player 1": S1.__name__,
                "Player 2": S2.__name__,
                "Score 1": score1,
                "Score 2": score2
            })


    # save results to csv with rounds in filename (avoid overwriting diff # of rounds)
    if save:
        filename = f"tournament_results_{rounds}rounds.csv"


        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Player 1", "Player 2", "Score 1", "Score 2"])
            writer.writeheader()
            writer.writerows(match_data)


            # put rankings at the bottom of the file
            writer.writerow({})
            writer.writerow({"Player 1": "final rankings (total score)"})
            for name, total in sorted(results.items(), key=lambda x: x[1], reverse=True):
                writer.writerow({"Player 1": name, "Score 1": total})


    # print summary in the console too
    print("\nfinal rankings:")
    for name, total in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"{name:25s} {total}")




if __name__ == "__main__":
    # run the tournament w/ rounds
    run_tournament(rounds=50)




