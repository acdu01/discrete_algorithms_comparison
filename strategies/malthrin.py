from strategies.base_strategy import Strategy

class Malthrin(Strategy):
    """Starts with cooperation, then defects if the opponent has defected in the first 7 rounds,
    mimics opponent's last move until round 98, then defects in the endgame."""
    def __init__(self):
        self.my_history = []
        self.opponent_history = []
        self.round = 0  # keeps track of round

    def move(self):
        if not self.opponent_history:
            return 'C'  # start with defect
        if self.round < 7:
            if 'D' in self.opponent_history:
                return 'D'  # if opponent has defected before in the first 7 rounds, always defect
            else:
                return 'C'  # otherwise, cooperate
        if self.round > 98:
            return 'D'  # endgame defect
        else:
            return self.opponent_history[-1]  # repeat opponent last move
        