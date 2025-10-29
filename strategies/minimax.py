from strategies.base_strategy import Strategy

POINTS = {
    ("C", "C"): (3, 3),  # both cooperate
    ("C", "D"): (0, 5),  # first cooperate, second betray
    ("D", "C"): (5, 0),  # first betray, second cooperate
    ("D", "D"): (1, 1),  # both betray
}


class MiniMax(Strategy):

    def __init__(self, rounds=2):
        super().__init__()
        self.rounds = rounds

    def move(self):

        if self.opponent_history:
            last_opponent_move = self.opponent_history[-1]
        else:
            last_opponent_move = "C"

        start_cooperation = self.minimax(
            "C", last_opponent_move, self.rounds, float("-inf"), float("inf"), True
        )
        start_deflection = self.minimax(
            "D", last_opponent_move, self.rounds, float("-inf"), float("inf"), True
        )

        return "C" if (start_cooperation > start_deflection) else "D"

    def minimax(self, my_move, opp_move, rounds, alpha, beta, maximize):

        if rounds == 0:
            return 0

        if maximize:
            max_points = float("-inf")
            opponent_moves = ["C", "D"]

            for opp_move in opponent_moves:

                current_round_score = POINTS[(my_move, opp_move)][0]
                future_round_score = self.minimax(
                    my_move, opp_move, rounds - 1, alpha, beta, False
                )
                total_score = current_round_score + future_round_score

                max_points = max(max_points, total_score)

                alpha = max(alpha, max_points)
                if alpha >= beta:
                    break

            return max_points

        else:
            min_points = float("inf")
            opp_next_move = ["C", "D"]

            for opp_next in opp_next_move:

                current_round_score = POINTS[(my_move, opp_next)][0]
                future_round_score = self.minimax(
                    my_move, opp_next, rounds - 1, alpha, beta, True
                )
                total = current_round_score + future_round_score
                min_points = min(min_points, total)

                beta = min(beta, min_points)
                if beta <= alpha:
                    break
            return min_points
