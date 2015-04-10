class Cuadruplo: 
    
    #Constructor
    def __init__(self):
        self.num     = 0
        self.opt = ''
        self.opd1 = ''
        self.opd2 = ''
        self.res   = ""

    #SETS & GETS
    def set_num(self, num): 
        self.num = num

    def set_opt(self, opt): 
        self.opt = opt

    def set_opd1(self, opd1):
        self.opd1 = opd1

    def set_opd2(self, opd2):
        self.opd2 = opd2

    def set_res(self, res):
        self.res = res

    def get_num(self): 
        return self.num

    def get_opt(self): 
        return self.opt

    def get_opd1(self):
        return self.opd1

    def get_opd2(self):
        return self.opd2

    def get_res(self):
        return self.res

    def print_cuadruplo(self):
        print(self.num, self.opt, self.opd1, self.opd2, self.res)


