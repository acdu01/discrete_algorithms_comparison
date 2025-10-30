from strategies.base_strategy import Strategy
import random

class RandomStrategy(Strategy):
    """Chooses 'C' or 'D' randomly with equal probability."""
    def move(self):
        return random.choice(['C', 'D'])