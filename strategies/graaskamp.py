from strategies.base_strategy import Strategy

class GraaskampStrategy(Strategy):
    """
    initially cooperates, then mimics opponent's last move for 50 rounds,
    defects once, mimics opponent's last move for 4 rounds,
    then analyzes opponent's behavior to decide whether to cooperate or defect
    based on their cooperation rate.
    """
    def move(self):
        if not self.my_history:
            return 'C'
        if len(self.my_history) <= 50:
            return self.opponent_history[-1]
        if len(self.my_history) == 51:
            return 'D'
        if len(self.my_history) <= 55:
            return self.opponent_history[-1]
        else:
            return self.check_strategy(self.opponent_history)


    def check_strategy(self, opponent_history):
        """check opponent strategy, if it seems to be a nice algorithm
        or itself, cooperate --- check history to see this
        if it seems to be random, defect"""
        coop_rate = opponent_history.count('C') / len(opponent_history)
        if coop_rate > 0.8:
            return 'C'
        else:
            return 'D'


