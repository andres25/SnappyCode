class Cuadruplo: 
    
    #Constructor
    def __init__(self, cNum, cOpt, cOpd1, cOpd2,cRes):
        self.num     = cNum
        self.opt = cOpt
        self.opd1 = cOpd1
        self.opd2 = cOpd2
        self.res   = cRes

    #SETS & GETS
    def setNum(self, num): 
        self.num = num

    def setOpt(self, opt): 
        self.opt = opt

    def setOpd1(self, opd1):
        self.opd1 = opd1

    def setOpd2(self, opd2):
        self.opd2 = opd2

    def setRes(self, res):
        self.res = res

    def getNum(self): 
        return self.num

    def getOpt(self): 
        return self.opt

    def getOpd1(self):
        return self.opd1

    def getOpd2(self):
        return self.opd2

    def getRes(self):
        return self.res

    def printCuad(self):
        print(self.num, '|', self.opt, '|', self.opd1, '|', self.opd2, '|', self.res , '\n')


