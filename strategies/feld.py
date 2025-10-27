from strategies.base_strategy import Strategy
import random

class Feld(Strategy):
    def __init__(self):
        self.my_history = []
        self.opponent_history = []
        self.probability = 1.0025

    def move(self):
        if not self.opponent_history: # start by cooperating
            return 'C'
        
        if self.probability > 0.5:
            self.probability -= 0.0025 # decrease probability so that it is 0.5 after 200 rounds

        if self.opponent_history[-1] == 'D': # opponent defected last round means defect
            return "D"
        else:
            if random.random() > self.probability: # if opponent cooperated, cooperate based on probability
                  return 'D'
            else:
                return 'C'