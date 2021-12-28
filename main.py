#!/usr/bin/env python
# coding: utf-8


import argparse
import magnets
import sys
import math
import os



parser = argparse.ArgumentParser()
# init_parameter-----------------------------------------------------------
# モデル用
parser.add_argument('--r', default = 2500, type=float) # 磁石半径[μm]
parser.add_argument('--thick', default = 1000, type=float) # 磁石厚さ[μm]
parser.add_argument('--gap', default = 200, type=float) # 磁石間ギャップ[μm]
parser.add_argument('--y', default = 9500, type=float) # 中央磁石の移動[μm]

parser.add_argument('--m', default = 26, type=float) # 磁石m角形近似
parser.add_argument('--n', default = 2, type=int) # 動かす磁石以外の磁石個数

# パス関連
parser.add_argument('path') # パスに入力したい名前
parser.add_argument('--filename', default = 'none')  # ファイル名

# -------------------------------------------------------------------------

args = parser.parse_args()

# コマンドライン引数を正しい型に変換
r = args.r
thick = args.thick
gap = args.gap
y = args.y
m = args.m
n = args.n
filename = args.filename

print('引数 r : ', r)  # 磁石半径[μm]
print('引数 thick: ', thick)  # 磁石厚さ[μm]
print('引数 gap : ', gap)  # 磁石間ギャップ[μm]
print('引数 y : ', y)  # 中央磁石の移動[μm]
print('引数 m : ', m)  # 磁石m角形近似
print('引数 n : ', n)  # 動かす磁石以外の磁石個数


# パス調整 - TODO: よしなにする
path = os.getcwd()
path = path + "\\" + str(filename)
path = path + '.Pin'


# 磁石配置用の計算をゴネゴネする - TODO: よしなにする
d = 2*((4*r + 2*gap)*math.cos(math.radians(45))) # 円形磁石間距離

z_ofst_1 = -thick/2 # 1つめ磁石Z軸オフセット
z_ofst_2 = -thick/2 # 2つめ磁石Z軸オフセット
z_ofst_3 = -thick/2 # 3つめ磁石Z軸オフセット

y_ofst_1 = 1000 + r # 1つめ磁石Y軸方向オフセット
y_ofst_2 = y + y_ofst_1 # 2つめ磁石Y軸方向オフセット
y_ofst_3 = y_ofst_1 + d/2 # 3つめ磁石Y軸方向オフセット

x_ofst_1 = 1000 + r # 1つめ磁石X軸オフセット
x_ofst_3 = x_ofst_1 + d/2 # 3つめ磁石X軸オフセット
x_ofst_2 = (x_ofst_1 + x_ofst_3)/2# 2つめ磁石X軸オフセット


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
Magnet1 = magnets.CircleMagnet(r=r, thick=thick, m=m, x_ofst=x_ofst_1, y_ofst=y_ofst_1, z_ofst=z_ofst_1, n=n, d=d, gap=gap, script=script, group_id=group_id, node_id=node_id)
## 円形磁石を配置する
Magnet1.plant()
## script, group_id, node_id を返してもらう
script, group_id, node_id = Magnet1.get_scripts()


## 2つ目の円形磁石オブジェクトを生成する
Magnet2 = magnets.CircleMagnet(r=r, thick=thick, m=m, x_ofst=x_ofst_2, y_ofst=y_ofst_2, z_ofst=z_ofst_2, n=n-1, d=d, gap=gap, script=script, group_id=group_id, node_id=node_id)
Magnet2.plant()
## 円形磁石を測定対象に指定する
Magnet2.measure_frustum()
script, group_id, node_id = Magnet2.get_scripts()

## 3つ目の円形磁石オブジェクトを生成する
Magnet3 = magnets.CircleMagnet(r=r, thick=thick, m=m, x_ofst=x_ofst_3, y_ofst=y_ofst_3, z_ofst=z_ofst_3, n=n, d=d, gap=gap, script=script, group_id=group_id, node_id=node_id)
Magnet3.plant()
script, group_id, node_id = Magnet3.get_scripts()


# ファイルに出力する
with open(path, "w") as f:
    f.write(script)
f.close()


# ***** プログラムおわり *****

