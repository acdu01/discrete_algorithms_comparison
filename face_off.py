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

    # return moves and scores
    return move1, move2, point1, point2


def play_game(p1, p2, rounds):
    total1 = total2 = 0
    p1_moves = []
    p2_moves = []
    
    # save moves and scores
    for _ in range(rounds):
        move1, move2, r1, r2 = play_round(p1, p2)
        total1 += r1
        total2 += r2
        p1_moves.append(move1)
        p2_moves.append(move2)

    # turn move lists into strings
    p1_history = ''.join(p1_moves)
    p2_history = ''.join(p2_moves)

    return total1, total2, p1_history, p2_history


if __name__ == "__main__":
    # set up two strategies to face off
    p1 = HarringtonStrategy()
    p2 = TitForTat()

    # run the simulation
    score1, score2, history1, history2 = play_game(p1, p2, 51)

    # print out the results
    print(f"Tournament result:")
    print(f"player 1 ({p1.__class__.__name__}): {score1}")
    print(f"player 2 ({p2.__class__.__name__}): {score2}")
    print(f"player 1 history: {history1}")
    print(f"player 2 history: {history2}")
