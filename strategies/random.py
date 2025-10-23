from strategies.base_strategy import Strategy
import random

class RandomStrategy(Strategy):
    def move(self):
        return random.choice(['C', 'D'])