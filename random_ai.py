"""
完全なランダム
"""

import random

class AI:
    def __init__(self):
        self.name = "Random AI" #勝敗表示に使われます

    @staticmethod
    def decide(_status):
        # status is like [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        # you have to return the position number: 0 to 5
        # 終了状態ではないことは前提して大丈夫です。
        decision = random.randrange(0, 6)
        while _status[decision] == 0:
            decision = random.randrange(0, 6)
        return decision
