from strategies.base_strategy import Strategy

class TitForTat(Strategy):
    def move(self):
        if not self.opponent_history:
            return 'C'  # start with cooperation
        return self.opponent_history[-1]  # repeat opponent last move