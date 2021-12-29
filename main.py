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
parser.add_argument('--r', default = 2500) # 磁石半径[μm]
parser.add_argument('--thick', default = 1000) # 磁石厚さ[μm]
parser.add_argument('--gap', default = 200) # 磁石間ギャップ[μm]
parser.add_argument('--y', default = 9500) # 中央磁石の移動[μm]

parser.add_argument('--m', default = 26) # 磁石m角形近似
parser.add_argument('--n', default = 2) # 動かす磁石以外の磁石個数

# パス関連
parser.add_argument('path') # パスに入力したい名前
parser.add_argument('--filename', default = 'none')  # ファイル名

# -------------------------------------------------------------------------

args = parser.parse_args()

# コマンドライン引数を正しい型に変換
r = float(args.r)
thick = float(args.thick)
gap = float(args.gap)
y = float(args.y)
m = float(args.m)
n = int(args.n)
filename = args.filename

print('引数 r : ', args.r)  # 磁石半径[μm]
print('引数 thick: ', args.thick)  # 磁石厚さ[μm]
print('引数 gap : ', args.gap)  # 磁石間ギャップ[μm]
print('引数 y : ', args.y)  # 中央磁石の移動[μm]
print('引数 m : ', args.m)  # 磁石m角形近似
print('引数 n : ', args.n)  # 動かす磁石以外の磁石個数


# パス調整 - TODO: よしなにする
path = os.getcwd()
path = path + "\\" + str(filename)
pin_path = path + '.Pin'
qit_path = path + '.Qit'


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
nMatcnt = 0
nDatcnt = 0
nID = 1

pin_script = ""
qit_script = ""


# 時候の挨拶
pin_script += f"""
solver Qm 5.00
scale 0.000001
#node番号表示
$nodenum grp on
"""

qit_script += f"""
[Title
sUser = "NOMAN"
sTitle = "Qm sim"
]

[Include
bLogList = F
bQic = T
]

[Solver
sName = StaticMagnetic
]

[Option
bAutoPanel = T
bPanelSaved = T
sPanelStat = POST
sMatrixSolver = MKL_LAPACK
]
"""

# 磁石を置く
## 1つ目の円形磁石オブジェクトを生成する
Magnet1 = magnets.CircleMagnet(r=r, thick=thick, m=m, x_ofst=x_ofst_1, y_ofst=y_ofst_1, z_ofst=z_ofst_1, n=n, d=d, gap=gap, pin_script=pin_script,
qit_script=qit_script, group_id=group_id, node_id=node_id, nMatcnt=nMatcnt, nDatcnt=nDatcnt, nID)
## 円形磁石を配置する
Magnet1.plant()
## 円形磁石を測定対象に指定する
Magnet1.measure_frustum()
## qitファイルを生成
Magnet1.make_qit_script()
## pin_script, qit_script, group_id, node_id, nMatcnt, nDatcnt, nID を返してもらう
pin_script, qit_script, group_id, node_id, nMatcnt, nDatcnt, nID = Magnet1.get_scripts()

# ファイルに出力する
with open(pin_path, "w") as f:
    f.write(pin_script)
f.close()
with open(qit_path, "w") as f:
    f.write(pin_script)
f.close()


# ***** プログラムおわり *****

