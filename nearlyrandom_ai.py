"""
横取りやピッタリゴールは優先され、それ以外はランダム。
"""

import random
import mancala

class AI:
    def __init__(self):
        self.name = "Nearly Random AI" #勝敗表示に使われます

    @staticmethod
    def decide(_status):
        result_list = []
        score_list = [0]*6
        for i in range(6):
            if _status[i] == 0:
                score_list[i] = -float("inf")
                result_list.append({"status":False, "goal":False, "again":False, "robbery":False})
                continue
            temp_status = _status.copy()
            temp_result = mancala.move(temp_status, i)
            if temp_result["robbery"] == True or temp_result["again"] == True:
                # 横取りやピッタリゴールが発生した時のみ、ゴールの玉の数の差異をスコアにする
                score_list[i] = temp_result["status"][6]-_status[6]
            else:
                # それ以外は0点
                score_list[i] = 0
            result_list.append(temp_result)
        # 最大値のものからランダムに選ぶ。特にピッタリゴールや横取りが無ければタダのランダム。
        return random.choice([i for i, x in enumerate(score_list) if x == max(score_list)])
