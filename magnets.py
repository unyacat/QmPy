# 各形の磁石を定義する

class CircleMagnet:
    def __init__(self, r, thick, m, x_ofst, y_ofst, z_ofst, n, gap, script, group_id, node_id, tri_r=200):
        self.r = r                 # 磁石半径[μm]
        self.thick = thick         # 磁石厚さ[μm]
        self.m = m                 # 磁石m角形近似
        self.x_ofst = x_ofst
        self.y_ofst = y_ofst
        self.z_ofst = z_ofst
        self.tri_r = tri_r         # 今回の円柱は三角形と四角形で構成されている。四角形と三角形について、どちらがどの分だけrを補うか計算。なるべく三角形の面積は小さいほうが良い。
        self.r_arg = float(360/m)  # 円分割角度[dig]
        self.n = n       # 動かす磁石以外の磁石個数
        self.d = 7 * r   # 円形磁石間距離
        self.rect_r = r  # 今回の円柱は三角形と四角形で構成されている。四角形と三角形について、どちらがどの分だけrを補うか計算。なるべく三角形の面積は小さいほうが良い。

        self.group_id = group_id
        self.node_id = node_id
        self.script = script
        self.zero = 0

        self.gap = gap   # 磁石間ギャップ[μm]
        self.x_QSf_ofst = self.r - gap/2
        self.y_QSf_ofst = self.r - gap/2
        self.z_QSf_ofst = self.thick / 2

        self.mw = self.r * 2 + gap * 2  # 測定面横
        self.ml = self.r * 2 + gap * 2  # 測定面縦

        self.quad_directions = [
            "0 -1 0",
            "-1 0 0",
            "0 1 0",
            "1 0 0",
            "0 0 1",
            "0 0 -1"
        ]

        self.quads = [
            [
                [self.zero - self.x_QSf_ofst, self.zero - self.y_QSf_ofst, self.zero - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.zero - self.y_QSf_ofst, self.zero - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.zero - self.y_QSf_ofst, self.thick + self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.zero - self.y_QSf_ofst, self.thick + self.z_QSf_ofst]
            ],
            [
                [self.zero - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   self.zero - self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.zero - self.y_QSf_ofst, self.zero - self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.zero - self.y_QSf_ofst, self.thick + self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   self.thick + self.z_QSf_ofst]
            ],
            [
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst, self.zero - self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.ml + self.y_QSf_ofst, self.zero - self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.ml + self.y_QSf_ofst, self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst, self.thick + self.z_QSf_ofst]
            ],
            [
                [self.mw + self.x_QSf_ofst, self.zero - self.y_QSf_ofst, self.zero - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   self.zero - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst, self.zero - self.y_QSf_ofst, self.thick + self.z_QSf_ofst]
            ],
            [
                [self.zero - self.x_QSf_ofst, self.zero - self.y_QSf_ofst,  self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.zero - self.y_QSf_ofst,  self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst,    self.thick + self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,    self.thick + self.z_QSf_ofst]
            ],
            [
                [self.mw + self.x_QSf_ofst,   self.zero - self.y_QSf_ofst, self.zero - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst,   self.zero - self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   self.zero - self.z_QSf_ofst],
                [self.zero - self.x_QSf_ofst, self.zero - self.y_QSf_ofst, self.zero - self.z_QSf_ofst]
            ]
        ]

    def plant(self):
        """
        磁石を配置する
        """

        self.script += f"""
        group {self.group_id} pnt
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        # pntは点
        xyz 0 0 0
        """
        self.group_id += 1
        self.script += f"""
        group {self.group_id} tri
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        xyz 0 0 0
        raz {self.tri_r} 0/{self.r_arg}:360
        # 半径tri_r　角度0開始r_arg増加　360終了　360/r=m角形になる
        tri 1 2:{self.m + 1} 3/
        # node1、node2~m_plus_1、node3~m_plus_1+1で三角形を定義
        copy group {self.group_id} dxyz 0 0/{self.d}::{self.n} 0
        # copyと反復を組み合わせる文はPクイックリファレンス2-96に記載されている
        # 繰り返し回数nをfloatにすると動作不安定になる（コンパイル(?)通るときと通らないときがある）
        """
        buffer = 30
        self.group_id += buffer
        self.script += f'''
        # copyにてgroup2:9を使用してしまっているため、以降でgroupを定義するときには9以上の数字を割り振る必要がある。今回は余裕をもって50にした。
        group {self.group_id} prism
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        select group {self.group_id - buffer}:{self.group_id - buffer + self.n}
        expand dz {self.thick}
        release all
        name QPn group {self.group_id}
        '''
        self.group_id += 1
        self.script += f'''
        group {self.group_id} quad
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        nd 1:{self.m + 1} ref {self.group_id - 30}@2/
        # node1~m_plus_1にgroup2のnode2の名前をつける（group3のnode1がgroup2のnode2を参照するため、割り振られる数字が一つずつずれる）
        raz {self.rect_r} 0/{self.r_arg}:360
        # 半径rect_r　角度開始r_arg増加　360終了　360/r=m角形になる
        quad 1:{self.m} {self.m + 2}/ {self.m + 3}/ 2/
        # node1~m、node m_plus_2~m_plus_2+m、node m_plus_3~m_plus_3+m、node2~m_plus_1で四角形を定義
        copy group {self.group_id} dxyz 0 0/{self.d}::{self.n} 0
        '''
        buffer = 10
        self.group_id += buffer

        self.script += f'''
        # 三角形を延長
        group {self.group_id} hexa
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        select group {self.group_id - buffer}:{self.group_id - buffer + self.n} 
        expand dz {self.thick}
        release all
        # 四角形を延長
        name QPn group {self.group_id}
        '''
        self.group_id += 1

    def measure(self):
        """
        オブジェクトを測定対象とする．
        """
        for i in range(6):
            self.script += self._generate_measurement_surface(self.quads[i], self.quad_directions[i])
        self.script += f"name QSf grp {self.group_id - 6}:{self.group_id - 1}"

    def _generate_measurement_surface(self, quad, direction):
        """
        測定面を1面生成する．
        内部で呼び出される関数．直接呼び出さない．
        """
        res = f"""
        grp {self.group_id} quad
        origin xyz {self.x_QSf_ofst} {self.y_QSf_ofst} {self.z_QSf_ofst}
        node {self.node_id} xyz {quad[0][0]} {quad[0][1]} {quad[0][2]}
        node {self.node_id + 1} xyz {quad[1][0]} {quad[1][1]} {quad[1][2]}
        node {self.node_id + 2} xyz {quad[2][0]} {quad[2][1]} {quad[2][2]}
        node {self.node_id + 3} xyz {quad[3][0]} {quad[3][1]} {quad[3][2]}
        quad nd {self.node_id} {self.node_id + 1} {self.node_id + 2} {self.node_id + 3}
        direction grp {self.group_id} along dxyz {direction}
        """

        self.group_id += 1
        self.node_id += 4

        return res

    def get_scripts(self):
        """
        オブジェクトが持っている script, group_id, node_id を取得する．
        他のオブジェクトに持っていく時は必ず最新の値を取得させ，それを渡す．
        """
        return self.script, self.group_id, self.node_id

