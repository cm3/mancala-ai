"""
4:1の割合で完全ランダムを混ぜた Nearly Random AI
"""

import random
import mancala
import random_ai
import nearlyrandom_ai

class AI:
    def __init__(self):
        self.name = "Nearly Random AI 2" #勝敗表示に使われます

    @staticmethod
    def decide(_status):
        return random_ai.AI.decide(_status) if random.randrange(0, 10)>=8 else nearlyrandom_ai.AI.decide(_status)
