from strategies.base_strategy import Strategy

class Davis(Strategy):
    """Only cooperates for the first 10 rounds, then checks the opponent's move history — if the opponent has defected in that time, Davis will solely defect from then onwards. Otherwise, it will only cooperate."""
    def __init__(self):
        self.my_history = []
        self.opponent_history = []   
        self.round = 0
 
    def move(self):       
        if self.round < 11:
            self.round += 1
            return 'C'  # cooperate for the first 10 rounds
        else:
            self.round += 1
            if 'D' in self.opponent_history:
                return 'D'  # if opponent ever defected, defect
            else:
                return 'C'  # otherwise, cooperate
