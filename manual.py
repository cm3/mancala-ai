"""
マニュアル入力
"""

import random

class AI:
    def __init__(self):
        self.name = "Manual input" #勝敗表示に使われます

    @staticmethod
    def decide(_status):
        decision = int(input("Which? (0-5): "))
        flag = False
        while flag == False:
            flag = True
            if decision not in list(range(6)):
                print("input number from 0 to 5")
                decision = int(input("Which? (0-5): "))
                flag = False
            elif _status[decision] == 0:
                print("Box "+str(decision)+" is empty.")
                decision = int(input("Which? (0-5): "))
                flag = False
        return decision
