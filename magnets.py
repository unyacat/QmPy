class CircleMagnet:
    def __init__(self, r, thick, m, x_ofst, y_ofst, z_ofst, n, d, gap, pin_script, qit_script, Mat_script, Dat_script, group_id, node_id, nMatcnt, nDatcnt, nID):
        self.r = r                 # 磁石半径[μm]
        self.thick = thick         # 磁石厚さ[μm]
        self.m = m                 # 磁石m角形近似
        self.x_ofst = x_ofst
        self.y_ofst = y_ofst
        self.z_ofst = z_ofst
        self.tri_r = r*0.4        # 今回の円柱は三角形と四角形で構成されている。四角形と三角形について、どちらがどの分だけrを補うか計算。なるべく三角形の面積は小さいほうが良い。
        self.r_arg = float(360/m)  # 円分割角度[dig]
        self.n = n       # 動かす磁石以外の磁石個数
        self.d = d
        
        self.rect_r = r  # 今回の円柱は三角形と四角形で構成されている。四角形と三角形について、どちらがどの分だけrを補うか計算。なるべく三角形の面積は小さいほうが良い。

        self.group_id = group_id
        self.node_id = node_id
        self.nMatcnt = nMatcnt
        self.nDatcnt = nDatcnt
        self.nID = nID
        self.pin_script = pin_script
        self.qit_script = qit_script
        self.Mat_script = Mat_script
        self.Dat_script = Dat_script
        
        # 四角形測定面関連
        self.gap = gap   # 磁石間ギャップ[μm]
        self.x_QSf_ofst = self.r - gap/2
        self.y_QSf_ofst = self.r - gap/2
        self.z_QSf_ofst = self.thick/2

        # 円形測定面関連
        self.x_QSf_ofst_frustum = self.x_ofst
        self.y_QSf_ofst_frustum = self.y_ofst
        self.z_QSf_ofst_frustum = self.z_ofst - gap/2
        
        self.QSf_r = self.r + gap/2
        self.QSf_thick = self.thick + gap

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
                [  - self.x_QSf_ofst,   - self.y_QSf_ofst,   - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,     - self.y_QSf_ofst,   - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,     - self.y_QSf_ofst, self.thick + self.z_QSf_ofst],
                [  - sLelf.x_QSf_ofst,   - self.y_QSf_ofst, self.thick + self.z_QSf_ofst]
            ],
            [
                [  - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,     - self.z_QSf_ofst],
                [  - self.x_QSf_ofst,   - self.y_QSf_ofst,   - self.z_QSf_ofst],
                [  - self.x_QSf_ofst,   - self.y_QSf_ofst, self.thick + self.z_QSf_ofst],
                [  - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   self.thick + self.z_QSf_ofst]
            ],
            [
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst,   - self.z_QSf_ofst],
                [  - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   - self.z_QSf_ofst],
                [  - self.x_QSf_ofst, self.ml + self.y_QSf_ofst, self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst, self.thick + self.z_QSf_ofst]
            ],
            [
                [self.mw + self.x_QSf_ofst,   - self.y_QSf_ofst,   - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst, self.ml + self.y_QSf_ofst,     - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst, self.ml + self.y_QSf_ofst,   self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   - self.y_QSf_ofst, self.thick + self.z_QSf_ofst]
            ],
            [
                [  - self.x_QSf_ofst,   - self.y_QSf_ofst,  self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,     - self.y_QSf_ofst,  self.thick + self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst,    self.thick + self.z_QSf_ofst],
                [  - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,    self.thick + self.z_QSf_ofst]
            ],
            [
                [self.mw + self.x_QSf_ofst,     - self.y_QSf_ofst,   - self.z_QSf_ofst],
                [self.mw + self.x_QSf_ofst,   self.ml + self.y_QSf_ofst,     - self.z_QSf_ofst],
                [  - self.x_QSf_ofst, self.ml + self.y_QSf_ofst,     - self.z_QSf_ofst],
                [  - self.x_QSf_ofst,   - self.y_QSf_ofst,   - self.z_QSf_ofst]
            ]
        ]
    
    
    def plant(self):
        """
        磁石を配置する
        """
        self.pin_script += f"""
        group {self.group_id} pnt
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        # pntは点
        xyz 0 0 0
        """
        self.group_id += 1
        self.pin_script += f"""
        group {self.group_id} tri
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        xyz 0 0 0
        raz {self.tri_r} 0/{self.r_arg}:360
        # 半径tri_r　角度0開始r_arg増加　360終了　360/r=m角形になる
        tri 1 2:{self.m + 1} 3/
        # node1、node2~m_plus_1、node3~m_plus_1+1で三角形を定義
        copy group {self.group_id} dxyz 0 0/{self.d}::{self.n} 0
        # copyと反復を組み合わせる文はPクイックリファレンス2-96に記載されている
        # 繰り返し回数nをfloatにすると動作不安定になる
        """
        buffer = 30
        n_buffer = 2
        self.group_id += buffer
        self.pin_script += f'''
        # 三角形を延長
        group {self.group_id} prism
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        select group {self.group_id - buffer}:{self.group_id - buffer + self.n}
        expand dz {self.thick}
        release all
        name QPn group {self.group_id}
        '''

        self.buf_Mat_script = f'''
        [Mat
        nID = {self.group_id}
        nID = {self.group_id}
        sTitle = "Mat{self.group_id}"
        nID = {self.nID}
        ]
        '''
        self.Mat_script += self.buf_Mat_script.strip("")
        self.buf_Mat_script = ""

        self.Dat_script += f'''
        [Dat
        sKind = MBH
        nID = {self.nID}
        sTitle = "ネオジム磁石N40のデータ"
        s2Unit = A/m T
        d2Factor = 1000000  1
        d2HB = -0.859  0
        d2HB = 0  1.285
        ]
        '''
        self.group_id += 1
        self.nID += 1
        self.nMatcnt += 1
        self.nDatcnt += 1

        self.pin_script += f'''
        group {self.group_id} quad
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        nd 1:{self.m + 1} ref {self.group_id - 30}@2/
        raz {self.rect_r} 0/{self.r_arg}:360
        # 半径rect_r　角度開始r_arg増加　360終了　360/r=m角形になる
        quad 1:{self.m} {self.m + 2}/ {self.m + 3}/ 2/
        # node1~m、node m_plus_2~m_plus_2+m、node m_plus_3~m_plus_3+m、node2~m_plus_1で四角形を定義
        copy group {self.group_id} dxyz 0 0/{self.d}::{self.n} 0
        '''
        buffer = 10
        self.group_id += buffer

        self.pin_script += f'''
        group {self.group_id} hexa
        origin xyz {self.x_ofst} {self.y_ofst} {self.z_ofst}
        select group {self.group_id - buffer}:{self.group_id - buffer + self.n}
        expand dz {self.thick}
        release all
        # 四角形を延長
        name QPn group {self.group_id}
        '''

        self.Mat_script += f'''
        [Mat
        nID = {self.group_id}
        sTitle = "Mat{self.group_id}"
        nID = {self.nID}
        ]
        '''
        self.Dat_script += f'''
        [Dat
        sKind = MBH
        nID = {self.nID}
        sTitle = "ネオジム磁石N40のデータ"
        s2Unit = A/m T
        d2Factor = 1000000  1
        d2HB = -0.859  0
        d2HB = 0  1.285
        ]
        '''
        self.group_id += 1
        self.nID += 1
        self.nMatcnt += 1
        self.nDatcnt += 1




    def measure_rect(self):
        """
        オブジェクトを四角形測定面で測定対象とする．
        """
        for i in range(6):
            self.pin_script += self._generate_measurement_surface(self.quads[i], self.quad_directions[i])[0]
            self.Mat_script += self._generate_measurement_surface(self.quads[i], self.quad_directions[i])[1]
            self.Dat_script += self._generate_measurement_surface(self.quads[i], self.quad_directions[i])[2]
        self.pin_script += f"name QSf grp {self.group_id - 6}:{self.group_id - 1}"
        

    def _generate_measurement_surface(self, quad, direction):
        ## pinファイル用
        """
        測定面を1面生成する．
        内部で呼び出される関数．直接呼び出さない．
        """
        res_pin_script = f"""
        grp {self.group_id} quad
        origin xyz {self.x_QSf_ofst} {self.y_QSf_ofst} {self.z_QSf_ofst}
        node {self.node_id} xyz {quad[0][0]} {quad[0][1]} {quad[0][2]}
        node {self.node_id + 1} xyz {quad[1][0]} {quad[1][1]} {quad[1][2]}
        node {self.node_id + 2} xyz {quad[2][0]} {quad[2][1]} {quad[2][2]}
        node {self.node_id + 3} xyz {quad[3][0]} {quad[3][1]} {quad[3][2]}
        quad nd {self.node_id} {self.node_id + 1} {self.node_id + 2} {self.node_id + 3}
        direction grp {self.group_id} along dxyz {direction}
        """

        ## qitファイル用
        self.nID += 600
        res_Mat_script = f"""
        [Mat
        nID = {self.group_id}
        sTitle = "Mat{self.group_id}"
        nDatID = {self.nID}
        ]
        """
        res_Dat_script = f'''
        [Dat
        sKind = MSpaceField
        nID = {self.nID}
        sTitle = "空間場(30*30)"
        n2Div = 30 30
        d2Ratio = 1 1
        n2Start = 0 0
        n2End = 0 0
        ]
        '''
        self.group_id += 1
        self.nID -= 599
        self.node_id += 4
        self.nMatcnt += 1
        self.nDatcnt += 1
        
        return res_pin_script, res_Mat_script, res_Dat_script

    def measure_frustum(self):
        """
        オブジェクトを円形測定面で測定対象とする．
        """
        for i in range(self.n):
            ## pinファイル用
            self.pin_script += f"""
            group {self.group_id} frustum
            origin xyz {self.x_QSf_ofst_frustum} {self.y_QSf_ofst_frustum} {self.z_QSf_ofst_frustum}
            cylinder cxyz 0 0 0 r {self.QSf_r} cxyz 0 0 {self.QSf_thick} r {self.QSf_r}
            name QSf grp {self.group_id}
            """
            self.y_QSf_ofst_frustum += self.d
            
            ## qitファイル用
            self.nID += 600
            self.Mat_script += f"""
            [Mat
            nID = {self.group_id}
            sTitle = "Mat{self.group_id}"
            nDatID = {self.nID}
            ]
            """
            self.Dat_script += f'''[Dat
            sKind = MSpaceField
            nID = {self.nID}
            sTitle = "円柱型空間場（30*30）"
            n2Div = 30 30
            d2Ratio = 1 1
            sSubCelDir = SelfCenter
            n2Start = 0 0
            n2End = 0 0
            ]
             '''
            self.group_id += 1
            self.nID -= 599
            self.nMatcnt += 1
            self.nDatcnt += 1

    def get_scripts(self):
        """
        オブジェクトが持っている pin_script, qit_script, Mat_script, Dat_script, group_id, node_id, nMatcnt, nDatcnt, nID を取得する．
        他のオブジェクトに持っていく時は必ず最新の値を取得させ，それを渡す．
        """
        return self.pin_script, self.qit_script, self.Mat_script, self.Dat_script, self.group_id, self.node_id, self.nMatcnt, self.nDatcnt, self.nID

