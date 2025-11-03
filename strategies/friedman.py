from strategies.base_strategy import Strategy

class Friedman(Strategy):
    """Starts by cooperating, but if the opponent ever defects, it will only defect onwards."""
    def move(self):
        if not self.opponent_history:
            return 'C'  # start with cooperation
        if 'D' in self.opponent_history:
            return 'D'  # if opponent has defected before, always defect
        else:
            return 'C'  # otherwise, cooperate
    