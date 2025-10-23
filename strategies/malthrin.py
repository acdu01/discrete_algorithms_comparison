from strategies.base_strategy import Strategy

class DefectTitForTat(Strategy):
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
        