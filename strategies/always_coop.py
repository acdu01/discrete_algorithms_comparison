from strategies.base_strategy import Strategy

class AlwaysCoop(Strategy):
    """always cooperate"""
    def move(self):
        return 'C'  