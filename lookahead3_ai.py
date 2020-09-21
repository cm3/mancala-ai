# 次の一手を読む
# ピッタリゴールを含めて、最も自陣の合計が多くなる方法を選ぶ
# 単にそれだけだと、ゴールに入れようとしないので、ゴールの点数を6倍扱い
# 2倍程度だと負けまくる

from copy import copy
import mancala
import random

class AI:
    def __init__(self):
        self.name = "Naive Greedy AI 3" #勝敗表示に使われます

    @staticmethod
    def decide_sub(_status, _original_status):
        """
        ピッタリゴールの再帰処理をするために、
        直前の状態と、元の状態を受け取って
        今回の判断と、最終状態を返す
        """
        result_list = [None]*6
        score_list = [0]*6
        for i in range(6):
            if _status[i] == 0:
                score_list[i] = -float("inf")
                result_list.append({"status":False, "goal":False, "again":False, "robbery":False})
                continue
            temp_status = _status.copy()
            temp_result = mancala.move(temp_status, i)
            if temp_result["again"] == True:
                if temp_result["goal"] == True:
                    return i, temp_result
                temp_decision, temp_result = AI.decide_sub(temp_result["status"], _original_status)
            score_list[i] = sum([x - y for (x, y) in zip(temp_result["status"][0:6], _original_status[0:6])]) + (temp_result["status"][6]-_original_status[6])*6
            result_list[i] = temp_result
        temp_decision = score_list.index(max(score_list))
        return temp_decision, result_list[temp_decision]

    @staticmethod
    def decide(_status):
        decision, status = AI.decide_sub(_status.copy(), _status.copy())
        return decision
