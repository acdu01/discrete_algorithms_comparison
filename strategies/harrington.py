import random
from strategies.base_strategy import Strategy

class HarringtonStrategy(Strategy):
    def __init__(self, initial_belief=0.5, belief_step=0.1, min_belief_to_cooperate=0.6, max_rounds_wait=20):
        super().__init__()
        self.belief = initial_belief  # how sure we are that the opponent is patient (likely to cooperate long-term)
        self.belief_step = belief_step  # how much we adjust our belief after each round
        self.min_belief_to_cooperate = min_belief_to_cooperate  # we only bother cooperating if belief is above this
        self.max_rounds_wait = max_rounds_wait  # how many rounds we’re willing to wait before giving up
        self.established_coop = False  # becomes true once both sides cooperate at least once
        self.defected_forever = False  # once this flips, never cooperate again

    def move(self):
        # if we've already given up on the opponent, always defect
        if self.defected_forever:
            return 'D'

        # once cooperation is established, we stick with it unless they defect
        if self.established_coop:
            if self.opponent_history and self.opponent_history[-1] == 'D':
                self.defected_forever = True
                return 'D'
            return 'C'

        # before cooperation is established
        round_number = len(self.my_history)

        # if belief gets too low or we've waited too long, just give up
        if self.belief < self.min_belief_to_cooperate or round_number >= self.max_rounds_wait:
            self.defected_forever = True
            return 'D'

        # otherwise, cooperate with a probability equal to our belief
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

        # if both cooperated this round, we can say cooperation is established
        if my_move == 'C' and opponent_move == 'C':
            self.established_coop = True
