"""
自分の手の結果を読む
ピッタリゴールを含めて、次に最もゴールに多く入る手を選ぶ
同列一位があった場合はなるべく相手に渡さない。
"""

from copy import copy
import mancala
import random

class AI:
    def __init__(self):
        self.name = "Naive Greedy AI 2" #勝敗表示に使われます

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
            score_list[i] = temp_result["status"][6]-_original_status[6]
            result_list[i] = temp_result
        if score_list.count(max(score_list)) == 1:
            temp_decision = score_list.index(max(score_list))
            return temp_decision, result_list[temp_decision]
        else:
            max_diff = max(score_list)
            for i in range(6):
                if score_list[i] == max_diff:
                    score_list[i] = sum([y - x for (x, y) in zip(result_list[i]["status"][7:14], _original_status[7:14])])
                else:
                    score_list[i] = -float("inf")
            temp_decision = score_list.index(max(score_list))
            return temp_decision, result_list[temp_decision]

    @staticmethod
    def decide(_status):
        decision, status = AI.decide_sub(_status.copy(), _status.copy())
        return decision
