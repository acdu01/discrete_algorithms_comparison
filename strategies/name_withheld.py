from strategies.base_strategy import Strategy
import random

class NameWithheld(Strategy):
    def __init__(self):
        self.my_history = []
        self.opponent_history = []   
        self.probibility = 0.3 # start probility at 0.3
        self.round = 0
        self.random_detector = 0
 
    def move(self):       
        if 'D' in self.opponent_history:
            fraction = self.opponent_history.count('D') / len(self.opponent_history) # fraction of opponent defections
        else:
            fraction = 0
        
        if self.round // 10 and self.opponent_history:   
            if fraction >= 0.6 and self.probibility >= 0.1: 
                self.probibility = self.probibility -0.1 # less cooperative if opponent defects a lot
            elif fraction < 0.4 and self.probibility <= 0.9:
                self.probibility = self.probibility +0.1 # more cooperative if opponent cooperates a lot
            else: 
                self.random_detector = 1 # detect random opponent if between 0.6 and 0.4 defections
        
        self.round += 1

        if self.random_detector == 1: # always defect if opponent is random
            return 'D'
        elif random.random() <= self.probibility: # cooperate based on probability
            return 'C'

        return 'D'