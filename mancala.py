from importlib import import_module
from copy import copy
import sys

def pretty_print(_status):
    print("    ["+str(_status[12]).rjust(2)+"]["+str(_status[11]).rjust(2)+"]["+str(_status[10]).rjust(2)+    "]["+str(_status[9]).rjust(2)+"]["+str(_status[8]).rjust(2)+"]["+str(_status[7]).rjust(2)+"]    ")
    print("["+str(_status[13]).rjust(2)+"]"+" "*4*6+"["+str(_status[6]).rjust(2)+"]")
    print("    ["+str(_status[0]).rjust(2)+"]["+str(_status[1]).rjust(2)+"]["+str(_status[2]).rjust(2)+    "]["+str(_status[3]).rjust(2)+"]["+str(_status[4]).rjust(2)+"]["+str(_status[5]).rjust(2)+"]    ")
    print()

def output_log(_file_stream,_record_per_game,_first,_second,winner):
    # didn't use csv package because the format is simple
    # didn't use json for enabling simple analysis using spreadsheets apps
    # didn't record so much information because this is enough for reproductivity
    fw.write(_record_per_game+"\t"+_first+"\t"+_second+"\t"+winner+"\n")

def move(_status, _decision):
    #自分側のポケットであることは**前提** それを元に手番を判断する。
    #ここでは各AIと違って、先手視点の盤面になっている(_decisionは7:13も入る)
    #何か入ってるか確認
    if _status[_decision] == 0:
        raise ValueError
    #相手のゴールポケットはスキップ
    skip = 6 if _decision//7==1 else 13
    just = 19 - skip #自分のゴール
    finish = False
    again = False
    robbery = False
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
    #ぴったりゴール確認
    if temp_position == just:
        again = True
    #横取り確認
    elif _status[temp_position] == 1 and 1 <= just-temp_position <= 6 and _status[12-temp_position] != 0:
        robbery = True
        _status[just] += _status[12-temp_position]
        _status[12-temp_position] = 0
    #ゲーム終了を確認
    if sum(_status[0:6])==0 or sum(_status[7:13])==0:
        finish = True
    return {"status":_status, "finish":finish, "again":again, "robbery":robbery}

def reverse_board(_status):
    temp_status = []*14
    temp_status[0:7] = _status[7:14]
    temp_status[7:14] = _status[0:7]
    return temp_status

def play(_first, _second):
    # 初期状態
    # ぐるぐる回るときに分かれているとややこしいので１次元配列
    # numpy は使っていない。学習時に必要ならば自分で np.array に入れて使って、.to_list して戻す。
    status = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    game_record = ""
    print("----START----")
    pretty_print(status)
    turn = 0 #内部ターンは0始まり、表示は+1しているので注意!
    print("----Turn "+str(turn+1)+"----")
    while True:
        decision = _first.decide(status) if turn%2 == 0 else _second.decide(reverse_board(status))+7
        game_record += str(decision) if turn%2 == 0 else str(decision-7)
        result = move(status, decision)
        status = result["status"]
        pretty_print(status)
        if result["robbery"] == True:
            print("Robbery!")
        if result["finish"] == True:
            break
        if result["again"] == False:
            turn += 1
            game_record += ","
            print("----Turn "+str(turn+1)+"----")
        else:
            print("Again!")
    p1_score = sum(status[0:7])
    p2_score = sum(status[7:14])
    print("Player 1: "+str(p1_score)+" Player 2: "+str(p2_score))
    if p1_score == p2_score:
        print("DRAW!")
        return 0, game_record
    elif p1_score > p2_score:
        print("Player 1 ("+_first.name+") WIN!!")
        return 1, game_record
    else:
        print("Player 2 ("+_second.name+") WIN!!")
        return -1, game_record

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Please specify your AI or \"manual\"")
    ai1 = import_module(sys.argv[1]).AI()
    ai2 = import_module(sys.argv[2]).AI()
    times = int(sys.argv[3]) if len(sys.argv) >= 4 else 1
    total_score = [0, 0]
    with open("log.tsv","a",encoding="utf8") as fw:
        for i in range(times):
            result, game_record = play(ai1, ai2)
            output_log(fw, game_record, ai1.name, ai2.name, str(result))
            if result != 0:
                total_score[int(1-(result+1)/2)] += 1  #1→0 -1→1
    print("\n\n\033[31mFinal Result:\033[0m")
    print("\033[34m"+ai1.name+"\033[0m \t"+str(total_score[0])+" win"+("s" if total_score[0]>=2 else "")+"!")
    print("\033[34m"+ai2.name+"\033[0m \t"+str(total_score[1])+" win"+("s" if total_score[1]>=2 else "")+"!")
