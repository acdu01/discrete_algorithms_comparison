from strategies.tit_for_tat import TitForTat
from strategies.harrington import HarringtonStrategy

POINTS = {
    ('C', 'C'): (3, 3),  # both cooperate
    ('C', 'D'): (0, 5),  # first cooperate, second betray
    ('D', 'C'): (5, 0),  # first betray, second cooperate
    ('D', 'D'): (1, 1)   # both betray 
}

def play_round(p1, p2):
    # each chooses a move based on strategy
    move1 = p1.move()
    move2 = p2.move()

    # look up what points each move combination gives
    point1, point2 = POINTS[(move1, move2)]

    # let each player update their internal state or belief
    p1.record_result(move1, move2)
    p2.record_result(move2, move1)

    return point1, point2

def play_game(p1, p2, rounds=200):
    # track total points across all rounds
    total1 = total2 = 0
    for _ in range(rounds):
        r1, r2 = play_round(p1, p2)
        total1 += r1
        total2 += r2
    return total1, total2

if __name__ == "__main__":
    # set up two strategies to face off
    p1 = HarringtonStrategy()
    p2 = TitForTat()

    # run the simulation
    score1, score2 = play_game(p1, p2, rounds=500)

    # print out the results
    print(f"Tournament result:")
    print(f"player 1 ({p1.__class__.__name__}): {score1}")
    print(f"player 2 ({p2.__class__.__name__}): {score2}")
