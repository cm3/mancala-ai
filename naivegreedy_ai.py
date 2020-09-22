"""
自分の手の結果を読む
ぴったりゴールがあればそれを
次に最もゴールに多く入る手を選ぶ
同列一位があった場合はなるべく相手に渡さない。
"""

from copy import copy
import mancala
import random

class AI:
    def __init__(self):
        self.name = "Naive Greedy AI" #勝敗表示に使われます

    @staticmethod
    def decide(_status):
        result_list = []
        score_list = [0]*6
        for i in range(6):
            if _status[i] == 0:
                score_list[i] = -float("inf")
                result_list.append({"status":False, "finish":False, "again":False, "robbery":False})
                continue
            temp_status = _status.copy()
            temp_result = mancala.move(temp_status, i)
            if temp_result["again"] == True:
                return i
            score_list[i] = temp_result["status"][6]-_status[6]
            result_list.append(temp_result)
        if score_list.count(max(score_list)) == 1:
            return score_list.index(max(score_list))
        else:
            max_diff = max(score_list)
            for i in range(6):
                if score_list[i] == max_diff:
                    score_list[i] = sum([y - x for (x, y) in zip(result_list[i]["status"][7:14], _status[7:14])])
                else:
                    score_list[i] = -float("inf")
        return score_list.index(max(score_list))
