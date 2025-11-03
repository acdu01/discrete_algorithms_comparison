from strategies.base_strategy import Strategy
import math

POINTS = {
    ('C', 'C'): (3, 3),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (1, 1)
}

class TidemanAndChieruzzi(Strategy):
    """
    A reactive strategy that mostly mirrors
    the opponent's last move, punishes streaks of defection, and occasionally
    attempts to reset the relationship.
    
    Starts cooperative and copies the opponent’s previous move. If the opponent defects 
    repeatedly, retaliates for the same number of rounds. When far ahead in score and 
    conditions look statistically unfavorable, performs a “fresh start” by cooperating 
    twice and clearing memory. Defects on the last two rounds to avoid endgame exploitation.
    """
    def __init__(self):
        super().__init__()
        self.retaliation_count = 0
        self.retaliation_remaining = 0
        self.last_fresh_start_round = -999
        self.total_rounds = 100  # updated externally by the tournament
        self.my_score = 0
        self.opponent_score = 0
        self.pending_fresh_start = 0  # counter for the two 'C's during fresh start

    def _calculate_scores(self):
        self.my_score = 0
        self.opponent_score = 0
        for m1, m2 in zip(self.my_history, self.opponent_history):
            s1, s2 = POINTS[(m1, m2)]
            self.my_score += s1
            self.opponent_score += s2

    def _opponent_defection_run(self):
        count = 0
        for move in reversed(self.opponent_history):
            if move == 'D':
                count += 1
            else:
                break
        return count

    def _fresh_start_conditions(self, rounds_left):
        # opponent is behind by at least 10 points
        if self.my_score - self.opponent_score < 10:
            return False
        # opponent has not just started a run of defections
        if self.opponent_history and self.opponent_history[-1] == 'D':
            return False
        # at least 20 rounds since last fresh start
        if len(self.my_history) - self.last_fresh_start_round < 20:
            return False
        # more than 10 rounds remaining
        if rounds_left <= 10:
            return False
        # opponent’s defections differ from 50–50 by ≥3σ
        n = len(self.opponent_history)
        if n < 10:
            return False
        d = self.opponent_history.count('D')
        expected = n / 2
        std = math.sqrt(n * 0.25)
        if abs(d - expected) < 3 * std:
            return False
        return True

    def move(self):
        round_num = len(self.my_history)
        rounds_left = self.total_rounds - round_num

        # defect on last two rounds
        if rounds_left <= 2:
            return 'D'

        # Pending cooperations for a fresh start
        if self.pending_fresh_start > 0:
            self.pending_fresh_start -= 1
            if self.pending_fresh_start == 0:
                # Reset memory after the two cooperations
                self.my_history.clear()
                self.opponent_history.clear()
                self.retaliation_count = 0
                self.retaliation_remaining = 0
                self.last_fresh_start_round = round_num
            return 'C'

        # If currently retaliating
        if self.retaliation_remaining > 0:
            self.retaliation_remaining -= 1
            return 'D'

        # If opponent just defected
        if self.opponent_history and self.opponent_history[-1] == 'D':
            run = self._opponent_defection_run()
            self.retaliation_count = max(self.retaliation_count, run)
            self.retaliation_remaining = self.retaliation_count
            return 'D'

        # Recalculate scores so far
        self._calculate_scores()

        # Check if fresh start conditions apply
        if self._fresh_start_conditions(rounds_left):
            self.pending_fresh_start = 2  # two cooperations
            return 'C'

        # Otherwise, mirror opponent’s last move or start with cooperation
        return self.opponent_history[-1] if self.opponent_history else 'C'
