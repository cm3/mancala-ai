import numpy as np
#import torch
import random

def pretty_print(_status):
    print("    ["+str(_status[12]).rjust(2)+"]["+str(_status[11]).rjust(2)+"]["+str(_status[10]).rjust(2)+    "]["+str(_status[9]).rjust(2)+"]["+str(_status[8]).rjust(2)+"]["+str(_status[7]).rjust(2)+"]    ")
    print("["+str(_status[13]).rjust(2)+"]"+" "*4*6+"["+str(_status[6]).rjust(2)+"]")
    print("    ["+str(_status[0]).rjust(2)+"]["+str(_status[1]).rjust(2)+"]["+str(_status[2]).rjust(2)+    "]["+str(_status[3]).rjust(2)+"]["+str(_status[4]).rjust(2)+"]["+str(_status[5]).rjust(2)+"]    ")
    print()

def move(_status, _decision):
    #自分側のポケットであることは**前提**
    #何か入ってるか確認
    if _status[_decision] == 0:
        raise ValueError
    #相手のゴールポケットはスキップ
    skip = 6 if _decision//7==1 else 13
    just = 19 - skip
    #動かす
    add = _status[_decision]
    _status[_decision] = 0 #まずコマを全部取る
    temp_position = _decision + 1
    while add > 0:
        temp_position = temp_position % 14
        if temp_position == skip:
            temp_position += 1
            temp_position = temp_position % 14
        _status[temp_position] += 1
        temp_position += 1
        add -= 1
    temp_position -= 1 #最後にいれた場所
    #ぴったりゴール　と　横取り　を確認。ぴったりゴールだと、次の番を自分で返す。
    again = True if temp_position == just else False
    if _status[temp_position] == 1 and just-temp_position >= 1 and just-temp_position <= 6 and _status[12-temp_position] != 0:
        print("Robbery!")
        _status[just] += _status[12-temp_position]
        _status[12-temp_position] = 0
    #上がったかどうかを確認
    if _status[0]==0 and _status[1]==0 and _status[2]==0 and _status[3]==0 and _status[4]==0 and _status[5]==0:
        goal = True
    elif _status[7]==0 and _status[8]==0 and _status[9]==0 and _status[10]==0 and _status[11]==0 and _status[12]==0:
        goal = True
    else:
        goal = False
    return {"status":_status, "goal":goal, "again":again}

def ai_random(_status, _is_first):
    place_shift = 0 if _is_first else 7
    decision = random.randrange(place_shift, 6+place_shift)
    while _status[decision] == 0:
        decision = random.randrange(place_shift, 6+place_shift)
    return decision

def play(_first, _second):
    # 初期状態
    # ぐるぐる回るときに分かれているとややこしいので１次元配列
    status = np.array([4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])
    print("----START----")
    pretty_print(status)
    turn = 0 #内部ターンは0始まり、表示は+1しているので注意!
    print("----Turn "+str(turn+1)+"----")
    while True:
        decision = _first(status, True) if turn%2 == 0 else _second(status, False)
        result = move(status, decision)
        status = result["status"]
        pretty_print(status)
        if result["goal"] == True:
            break
        if result["again"] == False:
            turn += 1
            print("----Turn "+str(turn+1)+"----")
        else:
            print("Again!")
    p1_score = sum(status[0:7])
    p2_score = sum(status[7:14])
    print("Player 1: "+str(p1_score)+" Player 2: "+str(p2_score))
    if p1_score == p2_score:
        print("DRAW!")
    elif p1_score > p2_score:
        print("Player 1 WIN!!")
    else:
        print("Player 2 WIN!!")

if __name__ == '__main__':
    play(ai_random,ai_random)
