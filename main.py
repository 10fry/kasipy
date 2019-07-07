from pykakasi import kakasi
import json
import pickle
import os

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
    else:
        return mes

def check(word,ls):
    wordch = "".join(word.split("１"))
    for i in ls:
        if "".join(i[0]) == wordch:
            return False
    return True

def evalScore(word1,word2):
    score = 0
    if len(word1) == len(word2):
        score += 2
    for i in range(len(word2)):
        if word1[i] == word2[i]:
            score += 10
        elif word1[i][-1] == word2[i][-1]:
            score += 3
        elif word1[i][:-1] == word2[i][:-1]:
            score += 2
        else:
            score += -7
    return score

def maxScore(ls):
    maxS = 1
    result = []
    for i in range(len(ls)):
        for j in range(len(ls[i][0])):
            if maxS <= ls[i][1][j]:
                maxS = ls[i][1][j]
                result.append([maxS,[i,j]])
    result.sort(key=lambda x :x[0],reverse=True)
    #print(result)
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
    return result

def main():
    ls = []
    print("command: (print/del/end)")
    print("")
    try:
        f = open("data.pickle",'rb')
        ls = pickle.load(f)
        print("Data:")
        for i in ls:
            print(i)
        print("")
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
        print("")
        print("Saved Data")
        for i in ls:
            print(i)
    except:
        pickle.dump(ls,file)
        f.close()
        print("Error occured.")
        #for i in ls:
        #   print(i)
    

if __name__ == '__main__':
    main()
