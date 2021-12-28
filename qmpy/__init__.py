from . import magnets


class Magnet:
    def __init__(self):
        self.scripts = []
        self.node_id = 1
        self.group_id = 1
        self.magnet = None

    def add(self, magnet: magnets.CircleMagnet):  # 一応書いてはいるが，将来的に他の形が導入されても型はチェックされないのである
        self.magnet = magnet
        magnet.plant()
        return self

    def measure_rect(self):
        if not self.magnet:
            raise ValueError()
        self.magnet.measure_rect()
        return self

    def measure_frustum(self):
        if not self.magnet:
            raise ValueError()
        self.magnet.measure_frustum()
        return self

    def get_scripts(self):
        return self.scripts

