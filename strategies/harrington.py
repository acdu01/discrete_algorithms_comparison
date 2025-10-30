import random
from strategies.base_strategy import Strategy

class HarringtonStrategy(Strategy):
    """
    maintains an internal "belief" about whether the opponent is
    patient and willing to cooperate long-term. At the beginning of the match,
    it explores cooperation probabilistically based on this belief. The belief
    increases when the opponent cooperates and decreases when they defect.
    """
    def __init__(self, initial_belief=0.5, belief_step=0.1, min_belief_to_cooperate=0.3):
        super().__init__()
        self.belief = initial_belief  # how sure we are that the opponent is patient (likely to cooperate long-term)
        self.belief_step = belief_step  # how much we adjust our belief after each round
        self.min_belief_to_cooperate = min_belief_to_cooperate  # we only bother cooperating if belief is above this
        self.established_coop = False  # becomes true once both sides cooperate at least once
        self.defected_forever = False  # once this flips, never cooperate again

    def move(self):
        # if it's already given up on the opponent, always defect
        if self.defected_forever:
            return 'D'

        # once cooperation is established, stick with it unless they defect
        if self.established_coop:
            if self.opponent_history and self.opponent_history[-1] == 'D':
                self.defected_forever = True
                return 'D'
            return 'C'

        # if belief gets too low just give up
        if self.belief < self.min_belief_to_cooperate:
            self.defected_forever = True
            return 'D'

        # otherwise, cooperate with a probability equal to belief
        coop_prob = self.belief
        if random.random() < coop_prob:
            return 'C'
        else:
            return 'D'

    def record_result(self, my_move, opponent_move):
        super().record_result(my_move, opponent_move)

        # update belief depending on what the opponent did
        if opponent_move == 'C':
            self.belief = min(1.0, self.belief + self.belief_step)
        else:
            self.belief = max(0.0, self.belief - self.belief_step)

        # if both cooperated this round, it can say cooperation is established
        if my_move == 'C' and opponent_move == 'C':
            self.established_coop = True

        
