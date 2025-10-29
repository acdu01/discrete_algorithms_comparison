from strategies.base_strategy import Strategy

class GraaskampStrategy(Strategy):
    """Initially cooperates in the first round.
    Copies what its opponent did in the previous round until round 50. 
    Defects in the 51st round to probe strategy weaknesses. 
    Plays tit for tat for another 5 moves. 
    Deflection on 51st round checks for itself/tit for tat strategies
    If the score is not good, it will assume that it is playing against random
    Otherwise, continue tit for tat but deflect every 5-15 moves

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


