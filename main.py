from pykakasi import kakasi
import json
import pickle
import os
import re
import copy
import shutil
import time

def help():
    print("command: help   (コマンド一覧を表示)")
    print("       : chg    (複数の文章を変換)")
    print("       : trans  (文を変換)")
    print("       : search (単語を変換)")
    print("       : reset  (一度使った単語を使わない機能をリセット)")
    print("       : dic    (辞書に単語を追加)")
    print("       : print  (辞書を表示)")
    print("       : del    (辞書の単語を削除)")
    print("       : end    (プログラムを終了)")
    print("")

def cmd(mes,ls,ka):
    if mes == "dic":
        print("return でコマンド入力画面に戻ります")
        print("")
        name = input("単語名:")
        while(True):
            if name == "return":
                break
            if check(name,ls) == True:
                ka.setMode('H', 'H')
                conv = ka.getConverter()
                jName = (conv.do(name)).split("１")
                ans = input("読み：{} ? (y/cancel/正しい読み) :".format(jName))
                if False == (ans == 'y' or ans == 'ｙ' or ans == ""):
                    jName = ans.split("１")
                    if (ans != "cancel"):
                        print(jName)
                ka.setMode('H', 'a')
                conv = ka.getConverter()
                tmpls = []
                for i in jName:
                    tmp = []
                    for j in i:
                        tmp.append(conv.do(j))
                    tmpls.append(tmp)
                name = name.split("１")
                if (ans != "cancel"):
                    ls.append([name,tmpls])
                    print("appended:",name,tmpls)
                else:
                    print("canceled")
            else:
                print("data exist.")
            print("")
            name = input("単語名:")
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "del":
        print("return でコマンド入力画面に戻ります")
        print("")
        delName = input("削除する単語：")
        if delName != "return":
            delItem = [i for i in ls if "".join(i[0]) == delName]
            if len(delItem) > 0:
                ls.remove(delItem[0])
                print("deleted:" + delName)
            else:
                print("No such data")
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "print":
        for i in ls:
            print(i)
        print("登録単語数: ",len(ls))
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "eval":
        ka.setMode('H', 'a')
        conv = ka.getConverter()
        word1 = conv.do(input("word1:"))
        word2 = conv.do(input("word2:"))
        print("Score({},{}): {}".format(word1,word2,evalScore(word1,word2)))
        print("")
        name = input("名前:")
        return cmd(name,ls,ka)
    elif mes == "getmax":
        getMaxLen(ls)
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)        
    elif mes == "search":
        rep = ["ー","っ","ゅ","ゃ","ょ"]
        print("return でコマンド入力画面に戻ります")
        print("")
        ka.setMode('H', 'H')
        conv = ka.getConverter()
        word = conv.do(input("サーチワード: "))
        while(True):
            if word == "return":
                break
            if ls == []:
                print("辞書が空です")
                break
            print(word)
            word = word.replace("しょ","そ")
            for i in rep:
                word = word.replace(i,"")
            wordls = []
            ka.setMode('H', 'a')
            conv = ka.getConverter()
            for i in word:
                wordls.append(conv.do(i))
            res = searchWord(wordls,ls)
            if len(res) >= 1:
                resWord = ""
                for i in res[:3]:
                    resWord += " [{}({}), {}]".format(ls[i[1][0]][0][i[1][1]],"".join(ls[i[1][0]][0]),i[0])
                print("類似ワード: " + resWord)
            else:
                print("類似ワードなし")
            print("")
            ka.setMode('H', 'H')
            conv = ka.getConverter()
            word = input("サーチワード: ")
            word = conv.do(word)
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "trans":
        print("return でコマンド入力画面に戻ります")
        flagTrans = True
        ans = input("変換した文章内の単語の重複を許しますか？(y/n) :")
        while(ans != "n" and ans!= "y"):
            ans = input("変換した文章内の単語の重複を許しますか？(y/n) :")
            if ans == "y":
                flagTrans = False
        print("")
        tempDic = copy.deepcopy(ls)
        ka.setMode('H', 'H')
        conv = ka.getConverter()
        kasi = ""
        while(True):
            ka.setMode('H', 'H')
            conv = ka.getConverter()
            kasi = input("歌詞を入力: ")
            if kasi == "return":
                break
            kasi = conv.do(kasi)
            print("歌詞の読みが以下でない場合、誤っている場所をひらがなに直してください。")
            print(kasi)
            ans = input()
            while(False == (ans == 'y' or ans == 'ｙ' or ans == "")):
                kasi = conv.do(ans)
                ans = input("この歌詞でよろしいですか？ (" + kasi + ") :")
            print("")
            transSnt(ls,ka,kasi,True,flagTrans)
        """
        while(kasi != "return"):
            if ls == []:
                print("辞書が空です")
                break
            if len(kasi) <= 1:
                print("類似ワードなし")
                print("")
            else:
                kasi = conv.do(kasi)
                print("歌詞の読みが以下でない場合、誤っている場所をひらがなに直してください。")
                print(kasi)
                tmpKasi = kasi
                tmpKasi = tmpKasi.replace("しょう","そ")
                tmpKasi = tmpKasi.replace("しょ","そ")
                for i in rep:
                    tmpKasi = tmpKasi.replace(i,"")
                #print(tmpKasi)
                tmpKasi = [tmpKasi]
                for i in esc:
                    kara = []
                    for j in tmpKasi:
                        tmpLs = j.split(i)
                        kara.extend(tmpLs)
                    tmpKasi = kara
                    #print(tmpKasi)
                tmpKasi = kara
                #print(kara)
                tmpKasi = [i for i in tmpKasi if i != ""]
                #print(tmpKasi)
                #print(kasi)
                ans = input()
                start = time.time()
                kasiLs = []
                while(False == (ans == 'y' or ans == 'ｙ' or ans == "")):
                    kasi = conv.do(ans)
                    ans = input("この歌詞でよろしいですか？ (" + kasi + ") :")
                    start = time.time()
                    tmpKasi = kasi
                    for i in rep:
                        tmpKasi = tmpKasi.replace(i,"")
                    print(tmpKasi)
                    tmpKasi = [tmpKasi]
                    for i in esc:
                        kara = []
                        for j in tmpKasi:
                            tmpLs = j.split(i)
                            kara.extend(tmpLs)
                        tmpKasi = kara
                        #print(tmpKasi)
                    tmpKasi = kara
                    #print(kara)
                    tmpKasi = [i for i in tmpKasi if i != ""]
                    #print(tmpKasi)
                for i in tmpKasi:
                    kaeuta, tempDic = trans(i, tempDic, ka, flagTrans)
                    #print(kaeuta)
                    kasiLs.append(kaeuta)
                #print(kasiLs)
                #歌詞の変換結果を表示
                nth = 0
                #print("kasi = ", kasi)
                #kasi = "".join(kasi)
                #print("kasiLs = ",kasiLs)
                #print("kara = ",kara)
                kasiNth = 0
                for j in kara:
                    if j == "":
                        print(kasi[nth:nth+1],end = "")
                        nth += 1
                    else:
                        for l in kasiLs[kasiNth]:
                            flagPrint = True
                            for m in rep:
                                if kasi[nth:nth+l[0]].count(m) == 1:
                                    flagPrint = False
                                    print(kasi[nth:nth+l[0]+1]+" ", end = "")
                                    nth += l[0] + 1
                            for m in range(l[0]):
                                try:
                                    if kasi[nth+m:nth+m+3] == "しょう":
                                        flagPrint = False
                                        print(kasi[nth:nth+l[0]+3]+" ", end = "")
                                        nth += l[0] + 1
                                except:
                                    pass
                            for m in range(l[0]):
                                try:
                                    if flagPrint and kasi[nth+m:nth+m+2] == "しょ":
                                        flagPrint = False
                                        print(kasi[nth:nth+l[0]+2]+" ", end = "")
                                        nth += l[0] + 1
                                except:
                                    pass
                            if flagPrint:
                                print(kasi[nth:nth+l[0]]+" ", end = "")
                                nth += l[0]
                        kasiNth += 1
                    nth += 1
                #for j in kasiLs:
                #    for i in j:
                #        print(kasi[nth:nth+i[0]]+" ", end = "")
                #        nth += i[0]
                print("")
                resWord = ""
                resWordReadable = ""
                for j in kasiLs:
                    for i in j:
                        resWord += "{}({}) ".format(ls[i[1][1][0]][0][i[1][1][1]], "".join(ls[i[1][1][0]][0]))
                        for l in ls[i[1][1][0]][1][i[1][1][1]]:
                            try:
                                resWordReadable += "{}".format(KtoH[l])
                            except:
                                resWordReadable += ""
                        resWordReadable += " "
                print(resWordReadable)
                print(resWord)
                end = time.time()
                print("[{}ms]".format(int(1000*(end - start))))
                print("")
                ka.setMode('H', 'H')
                conv = ka.getConverter()
            kasi = input("歌詞を入力: ")
        """
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "chg":
        flagTrans = True
        ans = input("変換した文章内の単語の重複を許しますか？(y/n) :")
        while(ans != "n" and ans!= "y"):
            ans = input("変換した文章内の単語の重複を許しますか？(y/n) :")
            if ans == "y":
                flagTrans = False
        tempDic = copy.deepcopy(ls)                
        while(True):
            print("変換したい文章を入力してください (入力終了：end/\\n 辞書をリセット:reset コマンド入力画面に戻る:return) ")
            st = input(":")
            if st == "return":
                print("")
                break
            if st == "reset":
                tempDic = copy.deepcopy(ls)
                print("")
            else:
                chgLs = []
                while(st != "end" and st != ""):
                    chgLs.append(st)
                    st = input(":")
                print("")
                for i in chgLs:
                    tempDic = transSnt(tempDic,ka,i,False,flagTrans)
                print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "reset":
        tempDic = copy.deepcopy(ls)
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "help":
        print("")
        help()
        name = input("コマンド:")
        return cmd(name,ls,ka)
    elif mes == "end":
        return mes
    else:
        print("無効なコマンドです")
        print("")
        name = input("コマンド:")
        return cmd(name,ls,ka)

def transSnt(ls,ka,kasi,displayFlag,flagTrans):
    KtoH = {"a":"あ","i":"い","u":"う","e":"え","o":"お",
            "ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ",
            "sa":"さ","shi":"し","su":"す","se":"せ","so":"そ",
            "ta":"た","chi":"ち","tsu":"つ","te":"て","to":"と",
            "na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の",
            "ha":"は","hi":"ひ","fu":"ふ","he":"へ","ho":"ほ",
            "ma":"ま","mi":"み","mu":"む","me":"め","mo":"も",
            "ya":"や","yu":"ゆ","yo":"よ",
            "ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ",
            "wa":"わ","wo":"を","n":"ん","vu":"ゔ",
            "ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
            "za":"ざ","zi":"じ","zu":"ず","ze":"ぜ","zo":"ぞ",
            "da":"だ","ji":"ぢ","de":"で","do":"ど",
            "ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ",
            "pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",}
    esc = [" ","　","、","。",",",".","[","]","「","」"]
    rep = ["ー","っ","ゅ","ゃ","ょ"]
    start = time.time()
    tempDic = copy.deepcopy(ls)
    ka.setMode('H', 'H')
    conv = ka.getConverter()
    if ls == []:
        print("辞書が空です")
    elif len(kasi) <= 1:
        print("類似ワードなし")
        print("")
    else:
        kasi = conv.do(kasi)
        tmpKasi = kasi
        tmpKasi = tmpKasi.replace("しょう","そ")
        tmpKasi = tmpKasi.replace("しょ","そ")
        for i in rep:
            tmpKasi = tmpKasi.replace(i,"")
        #print(tmpKasi)
        tmpKasi = [tmpKasi]
        for i in esc:
            kara = []
            for j in tmpKasi:
                tmpLs = j.split(i)
                kara.extend(tmpLs)
            tmpKasi = kara
            #print(tmpKasi)
        tmpKasi = kara
        #print(kara)
        tmpKasi = [i for i in tmpKasi if i != ""]
        #print(tmpKasi)
        #print(kasi)
        kasiLs = []
        for i in tmpKasi:
            kaeuta, tempDic = trans(i, tempDic, ka, flagTrans)
            #print(kaeuta)
            kasiLs.append(kaeuta)
        #print(kasiLs)
        #歌詞の変換結果を表示
        nth = 0
        #print("kasi = ", kasi)
        #kasi = "".join(kasi)
        #print("kasiLs = ",kasiLs)
        #print("kara = ",kara)
        kasiNth = 0
        #print(kara)
        for j in kara:
            for l in kasiLs[kasiNth]:
                flagPrint = True
                for m in rep:
                    if kasi[nth:nth+l[0]].count(m) == 1:
                        flagPrint = False
                        print(kasi[nth:nth+l[0]+1]+" ", end = "")
                        nth += l[0] + 1
                for m in range(l[0]):
                    try:
                        if kasi[nth+m:nth+m+3] == "しょう":
                            flagPrint = False
                            print(kasi[nth:nth+l[0]+3]+" ", end = "")
                            nth += l[0] + 2
                    except:
                        pass
                for m in range(l[0]):
                    try:
                        if flagPrint and kasi[nth+m:nth+m+2] == "しょ":
                            flagPrint = False
                            print(kasi[nth:nth+l[0]+2]+" ", end = "")
                            nth += l[0] + 1
                    except:
                        pass
                if flagPrint:
                    print(kasi[nth:nth+l[0]]+" ", end = "")
                    nth += l[0]
            if j != "":
                kasiNth += 1
            print(kasi[nth:nth+1],end = "")
            nth += 1
        #for j in kasiLs:
        #    for i in j:
        #        print(kasi[nth:nth+i[0]]+" ", end = "")
        #        nth += i[0]
        print("")
        resWord = ""
        resWordReadable = ""
        for j in kasiLs:
            for i in j:
                resWord += "{}({}) ".format(ls[i[1][1][0]][0][i[1][1][1]], "".join(ls[i[1][1][0]][0]))
                for l in ls[i[1][1][0]][1][i[1][1][1]]:
                    try:
                        resWordReadable += "{}".format(KtoH[l])
                    except:
                        resWordReadable += ""
                resWordReadable += " "
        print(resWordReadable)
        if displayFlag:
            print(resWord)
        end = time.time()
        #print("[{}ms]".format(int(1000*(end - start))))
    print("")
    return tempDic

def trans(kasi, ls, ka, flagTrans):
    escape = ["ん", "ー", "　", " "]
    maxlen = getMaxLen(ls)
    kaeuta = []
    nth = 0
    while(True):
        evalLs = []
        if nth >= len(kasi):
            break
        for i in range(1,maxlen):
            wordls = []
            ka.setMode('H', 'a')
            conv = ka.getConverter()
            try :
                ch = kasi[nth+i]
            except:
                ch = "あ"
            if len(kasi[nth+i:]) != 1 and escape.count(ch) == 0:
                for j in kasi[nth:nth+i]:
                    wordls.append(conv.do(j))
                res = searchWord(wordls,ls)
                if res:
                    evalLs.append([i,res[0]])
        evalLs.sort(key = lambda x: x[1][0], reverse=True)
        kaeuta.append(evalLs[0])
        if flagTrans:
            ls[evalLs[0][1][1][0]][0][evalLs[0][1][1][1]] = "ｑ"
            ls[evalLs[0][1][1][0]][1][evalLs[0][1][1][1]] = ["qq"]
        nth += evalLs[0][0]
    return kaeuta, ls

def getMaxLen(ls):
    maxlen = 0
    for i in ls:
        for j in range(len(i[0])):
            if maxlen < len(i[1][j]):
                maxlen = len(i[1][j])
    return maxlen

def check(word,ls):
    wordch = "".join(word.split("１"))
    for i in ls:
        if "".join(i[0]) == wordch:
            return False
    return True

def evalScore(name,kasi,init,sorset):
    score = 0
    offset = init
    lenKasi = len(kasi)
    lenName = len(name)
    #print(name, kasi)
    for i in range(lenKasi):
        if name[i+offset] == kasi[i]:
            # "ka" == "ka" 完全一致
            score += 12
        else:
            flag = False
            if kasi[i] == "tsu":
                score += -5
            #if ["a","i","u","e","o"].count(name[i+offset]) != 1:
            #    flag = True
            for j in sorset:
                if flag == False and j.count(name[i+offset][:-1]) == 1 and j.count(kasi[i][:-1]) == 1:
                    # 発音が似ているかをチェック
                    flag = True
                    break
            if name[i+offset][-1] == kasi[i][-1]:
                # 母音が一致
                score += 9
                if flag:
                    score += 2
            elif name[i+offset][:-1] == kasi[i][:-1] and kasi[i][:-1] != "":
                # 子音が一致
                score += 5
                if i == lenKasi-1:
                  score += -11
            elif flag:
                # 発音が似ている
                score += 2
                if i == lenKasi-1:
                  score += -11
            else:
#                try:
#                    if len(kasi[i+offset+1:]) >= len(kasi[i:]) and lenName != 1 and i != 0 and offset < 2:
#                        # 一文字ずらして探索
#                        scoreTmp = evalScore(word1[i+offset+1:i+offset+2],kasi[i:i+1],offset+1)
#                        if scoreTmp >= 0:
#                            offset += 1
#                            score -= 10
#                        score += scoreTmp
#                    else:
#                        score += -7
#                except:
                score += -7
            if score <= -10:
                return -1
    if lenKasi == 1:
        score += -3
    lenBonus = lenName-3
    if lenBonus >= 2:
        lenBonus = 2
    return round(score/lenName + lenBonus/2,2)

def maxScore(ls):
    maxS = 0
    result = []
    for i in range(len(ls)):
        for j in range(len(ls[i][0])):
            if maxS <= ls[i][1][j]:
                maxS = ls[i][1][j]
                result.append([maxS,[i,j]])
    result.sort(key=lambda x :x[0],reverse=True)
    return result

def searchWord(mes,ls):
    sorset = [["h","m","p","w","b"],["n","k","r"],["t","ts","ch","sh"],["t","ch","sh","s"],["d","r","t"],["h","b"]]
    scoreLs = []
    for i in range(len(ls)):
        scoreLs.append([ls[i][0],[]])
        for j in range(len(ls[i][0])):
            name = copy.deepcopy(ls[i][1][j])
            try:
                name.remove("n")
            except:
                pass
            if len(name) >= len(mes):
                scoreLs[i][1].append(evalScore(name,mes,0,sorset))
            else:
                scoreLs[i][1].append(0)
    result = maxScore(scoreLs)
    #print(result)
    return result

def main():
    ls = []
    help()
    try:
        f = open("data.pickle",'rb')
        ls = pickle.load(f)
        #print("Data:")
        #for i in ls:
        #    print(i)
        #print("")
        f.close()
    except:
        pass
#    try:
    file = open("data.pickle",'wb')
    ka = kakasi()
    ka.setMode('J', 'H')
    ka.setMode('K', 'H')
    ka.setMode('H', 'H')
    conv = ka.getConverter()
    name = cmd(input("コマンド:"),ls,ka)
    while(name != "end"):
        print("")
        name = cmd(input("コマンド:"),ls,ka)
    print("プログラムを終了します")
    pickle.dump(ls,file)
    f.close()
    shutil.copyfile("data.pickle","data.pickle.backup")
    #print("")
    #print("Saved Data")
    #for i in ls:
    #    print(i)
#    except:
#        pickle.dump(ls,file)
#        f.close()
#        shutil.copyfile("data.pickle","data.pickle.backup")
#        print("Error occured.")
#        #for i in ls:
#        #   print(i)
    

if __name__ == '__main__':
    main()
