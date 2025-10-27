from strategies.base_strategy import Strategy

class Grudger(Strategy):
    def move(self):       
        if 'D' in self.opponent_history:
            return 'D'  # if opponent ever defected, defect
        else:
            return 'C'  # otherwise, cooperate
