import sys
import random
import time
from collections import Counter

# 戦略についての数字との対応
# 0    :相手も含めた期待値最適化
# 1    :自分の損得最適化
# 2    :4以上の時はスキップせずそれ以外はスキップ、目は変えない
# 3以上:揃うまでダイスの目を変えずに投げ入れ続ける

def main(data):
    # ゲーム数を取り出し
    GameCount=int(data[0])
    
    # プレイヤー人数を配列の大きさから取り出し
    PlayerCount=len(data)-1
    
    # 各プレイヤーの現在の勝利数を初期化
    winner=[0 for i in range(PlayerCount)]
    
    # 各プレイヤーの戦略を配列化してGame関数に引き渡すために一度別配列にint型で取り出して格納
    player_data=[]
    for i in range(PlayerCount):
        player_data.append(int(data[i+1]))
    #print("playStyle")
    #print(player_data)
    
    # ゲーム数分だけGame関数を呼び出してWinner配列に結果を格納していく
    for i in range (GameCount):
        winner[Game(player_data)]+=1
    
    # 各プレイヤーの勝利数の配列を出力
    print(','.join(map(str,winner)))

def Game(player_data):
    # プレイヤー数を確認
    PlayerCount=len(player_data)

    # アリーナの状態を定義する配列
    Field = []
    
    # アリーナに初期ダイスを追加
    Field.append(random.randint(2, 6))
    
    # 各プレイヤーのもちダイス数を定義する配列
    player = []
    for i in range(PlayerCount):
        player.append(10-PlayerCount)
    
    # プレイヤーの手番を初期化
    turn=0
    
    # 敗戦済みのプレイヤーの数を定義
    DeathCount=0
    
    #無限ループ
    while 1==1:
    
        # 手持ちのダイスが0ならターンをスキップ
        if player[turn]<1:
            turn+=1
            turn=turn%PlayerCount
            continue
        
        # ダイスをひとつ投げ入れる
        # 投げ入れ方の戦略を決める
        if len(Field)==0: # AllInの箇所 強制
            for i in range(player[turn]):
                Field.append(random.randint(1, 6))
            player[turn]=0
        else: #AllIn以外の箇所
            # 変更するアリーナ上のダイスの数を決める変数
            ChangeDice=0
            
            # アリーナのダイスをいくつ変更するか
            if player_data[turn]==0: # 相手も含めた期待値最大化戦略
                if len(Field)<3: # アリーナのダイスが2以下の場合は一つ変更
                    ChangeDice=1
                else: # アリーナのダイスが3以上の場合、ダイスの数マイナス1変更
                    ChangeDice=len(Field)-1

                for i in range(ChangeDice): # 変更するダイスの数だけField配列からデータを削除
                    del Field[-1]

                for i in range(ChangeDice): # 変更するダイスの数だけField配列にデータを追加
                    Field.append(random.randint(1, 6))

            elif player_data[turn]==1: # 自分の損益最大化戦略
                if len(Field)==2: # アリーナのダイスが2の場合は一つ変更
                    ChangeDice=1
                elif len(Field)==3: # アリーナのダイスが2の場合は二つ変更
                    ChangeDice=2
                elif len(Field)>3: # アリーナのダイスが4以上の場合は三つ変更
                    ChangeDice=3

                for i in range(ChangeDice): # 変更するダイスの数だけField配列からデータを削除
                    del Field[-1]
                for i in range(ChangeDice): # 変更するダイスの数だけField配列にデータを追加
                    Field.append(random.randint(1, 6))

            # アリーナにダイスを一つ投げ入れる。
            player[turn]-=1
            Field.append(random.randint(1, 6))

        # 1を×とみなして1が出た数とその位置を記憶
        DelCount=[]
        position=0
        
        # 出目の1をすべて削除する ※配列を後ろから確認
        for i in range(len(Field)):
            position-=1
            if Field[position]==1:
                del Field[position]
                position+=1
        
        # ダイスの重複数を確認
        counter = Counter(Field)
        DicePlus=0
        
        # 重複したダイスの数を数える
        for item, count in counter.items():
            if count > 1:
                DicePlus+=count
        
        # 重複したダイスを獲得
        player[turn]+=DicePlus
        
        # ダイスの数が0になった場合そのプレイヤーは負け
        # 敗戦者がプレイヤー人数マイナス1以上になった時ゲーム終了
        if player[turn]==0:
            DeathCount+=1
            if DeathCount > PlayerCount-2:
                break
        
        # 重複したダイスを除いた配列を作成
        unique_array = [item for item in Field if counter[item] == 1]
        Field = unique_array.copy()
        
        skip=0
        # ダイス未獲得の場合もう一度投げ入れるかパスするかの選択
        # skip=1なら次のプレイヤーに手番を回す
        if DicePlus>0 or len(Field)<1 : #ダイスを獲得した場合とアリーナのダイスが0になった場合は強制的に次のプレイヤーに手番を回す
            skip=1
        else :
            if player_data[turn]==0: # 相手も含めた期待値最大化
                if len(Field) <2:
                    skip=1
            elif player_data[turn]==1: # 自分の損得を最適化する戦略
               if len(Field) <3:
                    skip=1
            elif player_data[turn]==2: # 4以上の時は投げ入れる
               if len(Field) <4:
                    skip=1
            else: # 獲得できるまで投げ入れる戦略
                skip=1

        # パスした場合と獲得した場合は次のプレイヤーに手番を回す。
        if skip==1:
            turn+=1
            turn=turn%PlayerCount
    
    # ゲーム終了時最大のダイスを持っている人の位置をreturnする
    max_value=max(player)
    
    return player.index(max_value)
 
if __name__ == '__main__':
    # 引数の数を確認、プレイ人数2～5に合わせて設定
    if len(sys.argv) < 4 or len(sys.argv) > 7:
        print("Error: wrong number of arguments")
        print("Usage: python <GameCount> {<PlaingPatern>...}*2～5")
        sys.exit()

    # 各引数がint型であるかどうかを確認
    for i in range(len(sys.argv)-1):
        test=sys.argv[i+1]
        if not test.isdigit():
            print(f"Error: is not integer '{test}'")
            sys.exit()
    
    # 一度引数を別の配列にコピーして先頭の実行ファイル部分を削除
    data=sys.argv.copy()
    del data[0]
    
    # メイン処理呼び出し
    main(data)


