from pykakasi import kakasi
import json
import pickle
import os
import re

def cmd(mes,ls,ka):
    if mes == "del":
        delName = input("デリートネーム：")
        delItem = [i for i in ls if "".join(i[0]) == delName]
        if len(delItem) > 0:
            ls.remove(delItem[0])
            print("deleted:" + delName)
        else:
            print("No data")
        print("")
        name = input("登録:")
        return cmd(name,ls,ka)
    elif mes == "print":
        for i in ls:
            print(i)
        print("")
        name = input("登録:")
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
        name = input("名前:")
        return cmd(name,ls,ka)        
    elif mes == "search":
        ka.setMode('H', 'H')
        conv = ka.getConverter()
        word = conv.do(input("サーチワード: "))
        while(True):
            print(word)
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
            if word == "return":
                break
            word = conv.do(word)
        print("")
        name = input("登録:")
        return cmd(name,ls,ka)
    elif mes == "trans":
        ka.setMode('H', 'H')
        conv = ka.getConverter()
        kasi = input("歌詞を入力: ")
        while(True):
            kasi = conv.do(kasi)
            print("歌詞の読みが以下でない場合、誤っている場所をひらがなに直してください。")
            print(kasi)
            kasi = re.split(' |　|、|。|,|\.',kasi)
            #print(kasi)
            ans = input()
            kasiLs = []
            while(False == (ans == 'y' or ans == 'ｙ' or ans == "")):
                kasi = conv.do(ans)
                ans = input("この歌詞でよろしいですか？ :" + kasi)
                kasi = re.split(' |　|、|。|,|.',kasi)
            for i in kasi:
                kaeuta = trans(i, ls, ka)
                #print(kaeuta)
                kasiLs.append(kaeuta)
            #print(kasiLs)
            nth = 0
            kasi = "".join(kasi)
            for j in kasiLs:
                for i in j:
                    print(kasi[nth:nth+i[0]]+" ", end = "")
                    nth += i[0]
            print("")
            resWord = ""
            for j in kasiLs:
                for i in j:
                    resWord += "{}({}) ".format(ls[i[1][1][0]][0][i[1][1][1]], "".join(ls[i[1][1][0]][0]))
            print(resWord)
            print("")
            ka.setMode('H', 'H')
            conv = ka.getConverter()
            kasi = input("歌詞を入力: ")
            if kasi == "return":
                break
        print("")
        name = input("登録:")
        return cmd(name,ls,ka)
    else:
        return mes

def trans(kasi, ls, ka):
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
        nth += evalLs[0][0]
    return kaeuta

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

def evalScore(word1,word2):
    score = 0
    offset = 0
    if len(word1) == len(word2) and len(word1) != 1:
        score += len(word1)
    for i in range(len(word2)):
        if word1[i+offset] == word2[i]:
            score += 10
        elif word1[i+offset][-1] == word2[i][-1]:
            score += 5
        elif word1[i+offset][:-1] == word2[i][:-1]:
            score += 3
        else:
            try:
                if len(word1[i+offset+1:]) >= len(word2[i:]) and len(word1) != 1 and i != 0 and offset < 2:
                    scoreTmp = evalScore(word1[i+offset+1:i+offset+2],word2[i:i+1])
                    if scoreTmp >= 0:
                        offset += 1
                        score -= 6
                    score += scoreTmp
            except:
                score += -7
    return round(score/len(word1),2)

def maxScore(ls):
    maxS = 1
    result = []
    for i in range(len(ls)):
        for j in range(len(ls[i][0])):
            if maxS <= ls[i][1][j]:
                maxS = ls[i][1][j]
                result.append([maxS,[i,j]])
    result.sort(key=lambda x :x[0],reverse=True)
    return result

def searchWord(mes,ls):
    scoreLs = []
    for i in range(len(ls)):
        scoreLs.append([ls[i][0],[]])
        for j in range(len(ls[i][0])):
            score = 0
            if len(ls[i][1][j]) >= len(mes):
                score += evalScore(ls[i][1][j],mes)
                scoreLs[i][1].append(score)
            else:
                scoreLs[i][1].append(0)
    result = maxScore(scoreLs)
    #print(result)
    return result

def main():
    ls = []
    print("command: (trans/search/print/del/end)")
    print("")
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
    try:
        file = open("data.pickle",'wb')
        ka = kakasi()
        ka.setMode('J', 'H')
        ka.setMode('K', 'H')
        ka.setMode('H', 'H')
        conv = ka.getConverter()
        name = cmd(input("登録:"),ls,ka)
        while(name != "end"):
            if check(name,ls) == True:
                ka.setMode('H', 'H')
                conv = ka.getConverter()
                jName = (conv.do(name)).split("１")
                ans = input("読み：{} ? input:".format(jName))
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
            name = cmd(input("登録:"),ls,ka)
        pickle.dump(ls,file)
        f.close()
        #print("")
        #print("Saved Data")
        #for i in ls:
        #    print(i)
    except:
        pickle.dump(ls,file)
        f.close()
        print("Error occured.")
        #for i in ls:
        #   print(i)
    

if __name__ == '__main__':
    main()
