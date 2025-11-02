from strategies.base_strategy import Strategy

POINTS = {
    ("C", "C"): (3, 3),  # both cooperate
    ("C", "D"): (0, 5),  # first cooperates, second betrays
    ("D", "C"): (5, 0),  # first betrays, second cooperates
    ("D", "D"): (1, 1),  # both betray
}


class MaxMax(Strategy):
    def __init__(self, rounds=5):
        super().__init__()
        self.rounds = rounds  # how many future rounds to look ahead

    def move(self):
        # check how good it would be to start with cooperation
        start_cooperation = self.minimax(
            "C", True, self.rounds, float('-inf'), float('inf')
        )
        # check how good it would be to start with defection
        start_deflection = self.minimax(
            "D", True, self.rounds, float('-inf'), float('inf')
        )

        # pick the move with the better expected score
        return "C" if (start_cooperation >= start_deflection) else "D"

    def minimax(self, my_move, maximize, rounds_left, alpha, beta):
        # stop if there are no rounds left to simulate
        if rounds_left == 0:
            return 0

        if maximize:
            # its turn, try to maximize score
            max_points = float('-inf')
            for opp_move in ["C", "D"]:
                # get score for this round based on both of its moves
                score = POINTS[(my_move, opp_move)][0]
                # simulate what happens next if opponent plays next
                eval = score + self.minimax(opp_move, False, rounds_left - 1, alpha, beta)
                # keep the best possible total
                max_points = max(max_points, eval)
                # update alpha for pruning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # prune if no better outcome is possible
            return max_points

        else:
            # assume opponent maximizes their own score, not minimizes its
            max_points = float('-inf')
            for my_next_move in ["C", "D"]:
                score = POINTS[(my_next_move, my_move)][0]
                eval = score + self.minimax(my_next_move, True, rounds_left - 1, alpha, beta)
                max_points = max(max_points, eval)
            return max_points
