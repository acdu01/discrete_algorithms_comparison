class Strategy:
    def __init__(self):
        self.my_history = []
        self.opponent_history = []

    def move(self):
        """
        Return 'C' or 'D'
        """
        raise NotImplementedError

    def record_result(self, my_move, opponent_move):
        """
        Store what happened that round
        """
        self.my_history.append(my_move)
        self.opponent_history.append(opponent_move)