import random
from strategies.base_strategy import Strategy

class GrofmanStrategy(Strategy):
    def move(self):
        """
        start with cooperating
        if the players did different things, cooperates with 2/7 probability
        otherwise cooperates
        """
        if not self.opponent_history:
            return 'C'
        if self.my_history[-1] != self.opponent_history[-1]:
            if random.random() < 2/7:
                return 'C' 
            else:
                return 'D'
        return 'C'