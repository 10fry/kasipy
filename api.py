# 必要なモジュールの読み込み
from flask import Flask, jsonify, abort, make_response, request
import kasipy
import pickle
from pykakasi import kakasi

# Flaskクラスのインスタンスを作成
# __name__は現在のファイルのモジュール名
api = Flask(__name__)

# GETの実装
@api.route('/get', methods=['GET'])
def get():
    result = { "greeting": 'hello flask' }
    return make_response(jsonify(result))

@api.route("/trans/<text>")
def trans(text):
    kaeuta = kasipy.trans(text, ls, ka)
    nth = 0
    kasi = ""
    for i in kaeuta:
        kasi += text[nth:nth+i[0]]+" "
        nth += i[0]
    resWord =  kasi + "\n"
    for i in kaeuta:
        resWord += "{}({}) ".format(ls[i[1][1][0]][0][i[1][1][1]], "".join(ls[i[1][1][0]][0]))
    print(resWord)
    return resWord

# エラーハンドリング
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# ファイルをスクリプトとして実行した際に
# ホスト0.0.0.0, ポート3001番でサーバーを起動
if __name__ == '__main__':
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
    ka = kakasi()
    ka.setMode('J', 'H')
    ka.setMode('K', 'H')
    ka.setMode('H', 'H')
    api.run(host='0.0.0.0', port=3001)
