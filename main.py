from pykakasi import kakasi
import json
import pickle
import os

def cmd(mes,ls):
    if mes == "del":
        delName = input("デリートネーム：")
        delItem = [i for i in ls if "".join(i[0]) == delName]
        if len(delItem) > 0:
            ls.remove(delItem[0])
            print("deleted:" + delName)
        else:
            print("No data")
        print("")
        name = input("名前:")
        return cmd(name,ls)
    elif mes == "print":
        for i in ls:
            print(i)
        print("")
        name = input("名前:")
        return cmd(name,ls)
    else:
        return mes

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
        name = cmd(input("名前:"),ls)
        ka.setMode('J', 'H')
        ka.setMode('K', 'H')
        ka.setMode('H', 'H')
        conv = ka.getConverter()
        while(name != "end"):
            ka.setMode('H', 'H')
            conv = ka.getConverter()
            jName = (conv.do(name)).split("１")
            ans = input("読み：{} ? input:".format(jName))
            if False == (ans == 'y' or ans == 'ｙ' or ans == ""):
                jName = ans.split("１")
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
            ls.append([name,tmpls])
            print("appended:",name,tmpls)
            print("")
            name = cmd(input("名前:"),ls)
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
        for i in ls:
           print(i)
    

if __name__ == '__main__':
    main()
