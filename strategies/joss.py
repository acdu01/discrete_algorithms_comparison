from strategies.base_strategy import Strategy
import random

class JossStrategy(Strategy):
    """Starts with cooperation, then mimics opponent's last move,
    but with a small probability of defecting randomly."""
    def move(self):
        if not self.opponent_history:
            return 'C' # begin with cooperation
        
        else:
            if random.random() < 0.1:
                return 'D' # 10 percent chance to defect

            return self.opponent_history[-1]
