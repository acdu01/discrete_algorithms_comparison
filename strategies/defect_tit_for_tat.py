from strategies.base_strategy import Strategy

class DefectTitForTat(Strategy):
    """starts with defect, then mimics opponent's last move"""
    def move(self):
        if not self.opponent_history:
            return 'D'  # start with defect
        return self.opponent_history[-1]  # repeat opponent last move