from class_extend.line.bline import Bline


class Cline(Bline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.circle1 = self.obj_1

    def def_ptdeb_ptfin(self):
        self.ptdebut = self.obj_1.get_center()
        self.ptfin = self.obj_2.get_center()

    def update_ptsdebut_fin(self):
        self.ptdebut = self.obj_1.get_center()
        self.ptfin = self.obj_2.get_center()
