#!/usr/bin/env python
# coding: utf-8


import argparse
import magnets


parser = argparse.ArgumentParser()
# init_parameter-----------------------------------------------------------
# モデル用
parser.add_argument('--r', default = 2500) # 磁石半径[μm]
parser.add_argument('--thick', default = 1000) # 磁石厚さ[μm]
parser.add_argument('--gap', default = 200) # 磁石間ギャップ[μm]
parser.add_argument('--y', default = 9500) # 中央磁石の移動[μm]
parser.add_argument('--init_y', default = 9500) # シミュレーションを開始する際の初期位置 いらないかもしれない

parser.add_argument('--m', default = 26) # 磁石m角形近似
parser.add_argument('--n', default = 2) # 動かす磁石以外の磁石個数

# 測定面用
parser.add_argument('--mw', default = 10000) # 測定面用幅
parser.add_argument('--ml', default = 10000) # 測定面用高さ

# パス関連
# parser.add_argument('path', default="output.txt")  # パスに入力したい名前

parser.add_argument('--filename', default = 'none')  # ファイル名

# -------------------------------------------------------------------------

args = parser.parse_args()

# コマンドライン引数を正しい型に変換
r = float(args.r)
thick = float(args.thick)
gap = float(args.gap)
y = float(args.y)
init_y = float(args.init_y)
m = float(args.m)
n = int(args.n)
mw = float(args.mw)
ml = float(args.ml)
filename = args.filename

print('引数 r : ', args.r)  # 磁石半径[μm]
print('引数 thick: ', args.thick)  # 磁石厚さ[μm]
print('引数 gap : ', args.gap)  # 磁石間ギャップ[μm]
print('引数 y : ', args.y)  # 中央磁石の移動[μm]
print('引数 init_y : ', args.init_y)  # シミュレーションを開始する際の初期位置 いらないかもしれない
print('引数 m : ', args.m)  # 磁石m角形近似
print('引数 n : ', args.n)  # 動かす磁石以外の磁石個数
print('引数 mw : ', args.mw)  # 測定面用幅
print('引数 ml : ', args.ml)  # 測定面用高さ


# パス調整 - TODO: よしなにする
# date = datetime.datetime.now()
# path = os.getcwd()
# path = path + "\\" + str(filename)
# path = path + '.Pin'
path = "output.txt"


# ***** プログラムここから *****

group_id = 1
node_id = 1
script = ""


# 時候の挨拶
script += f"""#solverは未定義でQm5.00が指定される
solver Qm 5.00
scale 0.000001
#node番号表示
$nodenum grp on
"""

# 磁石を置く
## 1つ目の円形磁石オブジェクトを生成する
Magnet1 = magnets.CircleMagnet(r=r, thick=thick, m=m, x_ofst=100, y_ofst=200, z_ofst=300, n=n, gap=gap, script=script, group_id=group_id, node_id=node_id)
## 円形磁石を配置する
Magnet1.plant()
## 円形磁石を測定対象に指定する
Magnet1.measure()
## script, group_id, node_id を返してもらう
script, group_id, node_id = Magnet1.get_scripts()


## 2つ目の円形磁石オブジェクトを生成する
Magnet2 = magnets.CircleMagnet(r=r, thick=thick, m=m, x_ofst=200, y_ofst=300, z_ofst=400, n=n, gap=gap, script=script, group_id=group_id, node_id=node_id)
## 円形磁石を配置する
Magnet2.plant()
## script, group_id, node_id を返してもらう
script, group_id, node_id = Magnet2.get_scripts()


# ファイルに出力する
with open(path, "w") as f:
    f.write(script)
f.close()


# ***** プログラムおわり *****

