from strategies.base_strategy import Strategy

class AlwaysDefect(Strategy):
    """always defect"""
    def move(self):
        return 'D'  