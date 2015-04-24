from varGlobales import *
from procVarTables import *
from memory import *
import turtle

cuadEjec = 0
memEntero = 0
memFlotante = 0
memTexto = 0
memBooleano = 0

# grapgics turtle
turtle.setup(800, 600)
wn = turtle.Screen()
wn.title("SnappyCode")
tess = turtle.Turtle()
wn.exitonclick()

pilaSaltosEjec = []
pilaVarTableLocSpace = []
pilaVarTableLocSpaceName = []
def getOperand(cuadruplo, num):
	if (num == 1):
		opdDir = cuadruplo.opd1
	else:
		opdDir = cuadruplo.opd2

	if opdDir == None:
		return

	isVar = True
	while isVar:
		if opdDir == None:
			return
		elif opdDir >= 0 and opdDir < 4000:
			for var in varGlb:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		elif opdDir >= 4000 and opdDir < 7000:
			for proc in procTable:
				for var in proc.procVars:
					if var.varDir == opdDir:
						opdVar = var
						opdDir = var.varVal
		elif opdDir >= 7000 and opdDir < 12000:
			for var in tempTable:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		elif opdDir >= 12000 and opdDir < 16000:
			isVar = False

	for cons in consTable:
		if cons.consDir == opdDir:
			return cons.consVal

def getResult(cuadruplo):
	opdDir = cuadruplo.res
	if opdDir == None:
		return
	elif opdDir >= 0 and opdDir < 4000:
		for var in varGlb:
			if var.varDir == opdDir:
				return var
	elif opdDir >= 4000 and opdDir < 7000:
		for proc in procTable:
			for var in proc.procVars:
				if var.varDir == opdDir:
					return var
	elif opdDir >= 7000 and opdDir < 12000:
		for var in tempTable:
			if var.varDir == opdDir:
				return var

def prepRes(cVal, cType):
	global memEntero
	global memFlotante
	global memTexto
	global memBooleano
	consDir = consGetDir(cVal)
	if consDir == None:
		if cType == 'entero':
			memEntero = memEntero+1
			mem = memEntero
		elif cType == 'flotante':
			memFlotante = memFlotante+1
			mem = memFlotante
		elif cType == 'texto':
			memTexto = memTexto+1
			mem = memTexto
		elif cType== 'booleano':
			memBooleano = memBooleano+1
			mem = memBooleano
		consInsert(cVal, cType, mem)
	consDir = consGetDir(cVal)
	return consDir

def initMem():
	global memEntero
	global memFlotante
	global memTexto
	global memBooleano
	for cons in consTable:
		if cons.consType == 'entero':
			if cons.consDir > memEntero:
				memEntero = cons.consDir
		elif cons.consType == 'flotante':
			if cons.consDir > memFlotante:
				memFlotante = cons.consDir
		elif cons.consType == 'texto':
			if cons.consDir > memTexto:
				memTexto = cons.consDir
		elif cons.consType == 'booleano':
			if cons.consDir > memBooleano:
				memBooleano = cons.consDir

def getCuadMain():
	for proc in procTable:
		if proc.procName == 'main':
			return proc.procDir

def getProcByJumpDir(jumpDir):
	for proc in procTable:
		if proc.procDir == jumpDir:
			return proc

def setParam(varDir, jumpDir, numparem):
	paramsFunc = None
	procVars = None
	proc = getProcByJumpDir(jumpDir)
	paramsFunc = proc.procParams.copy()
	procVars = proc.procVars
	paramsFunc[numparem].varVal = varDir
	procVars.append(paramsFunc[numparem])

def InterpretarCuadruplos():
	global tess
	x = getCuadMain()
	initMem()
	while x < len(cuadruplos):
		opt = cuadruplos[x].opt
		num = cuadruplos[x].num
		if opt == 'GOTO':
			if cuadruplos[x].res == 1:
				y = x + 1
				opt = cuadruplos[y].opt
				numParam = 0
				saltoProc = cuadruplos[x].opd2
				proc = getProcByJumpDir(saltoProc)
				auxVarTable = proc.procVars.copy()
				pilaVarTableLocSpace.append(auxVarTable)
				pilaVarTableLocSpaceName.append(proc.procName)
				while opt == 'PARAM':
					setParam(cuadruplos[y].opd1,saltoProc,numParam)
					numParam = numParam + 1
					y = y + 1
					opt = cuadruplos[y].opt
				pilaSaltosEjec.append(y)
			x = cuadruplos[x].opd2
		elif opt == 'GOTOF':
			val = getOperand(cuadruplos[x], 1)
			if val == 0:
				x = cuadruplos[x].opd2
			else:
				x = x + 1
		elif opt == 'RETURN':
			x = pilaSaltosEjec.pop()
			procName = pilaVarTableLocSpaceName.pop()
			proc = getProc(procName)
			auxVarTable = pilaVarTableLocSpace.pop()
			proc.procVars = auxVarTable
		elif opt == 'PRINT':
			opd1 = getOperand(cuadruplos[x], 1)
			x = x +1
			print (opd1)
		elif opt == 'MOVER':
			tess.forward(getOperand(cuadruplos[x], 1))
			print('MOVER')
			x = x+1
		elif opt == 'PINTAR':
			tess.pendown()
			print('PINTAR')
			x = x+1
		elif opt == 'DESPINTAR':
			tess.penup()
			print('DESPINTAR')
			x = x+1
		elif opt == 'BORRAR':
			tess.reset()
			print('BORRAR')
			x = x+1
		elif opt == 'GIRARDERECHA':
			tess.right(getOperand(cuadruplos[x], 1))
			print('GIRARDERECHA')
			x = x+1
		elif opt == 'GIRARIZQUIERDA':
			tess.left(getOperand(cuadruplos[x], 1))
			print('GIRARIZQUIERDA')
			x = x+1
		elif opt == '=':
			opdDir = cuadruplos[x].opd1
			resVar = getResult(cuadruplos[x])
			resVar.varVal = opdDir
			print (num,"|",opdDir,"|",None,"|",opt,"|",resVar.varDir,"\n")
			x = x+1
		else:
			opd1 = getOperand(cuadruplos[x], 1)
			opd2 = getOperand(cuadruplos[x], 2)
			resVar = getResult(cuadruplos[x])

			#Arithmetic
			if opt == "+" :
				res = opd1 + opd2
			elif opt == "-":
				res = opd1 - opd2
			elif opt == "*":
				res = opd1 * opd2
			elif opt == "/":
				if opd2 == 0:
					print("Error: No puede realizar divisiones entre 0. ")
					sys.exit()
				elif resVar.varType == 'entero':
					res = opd1 // opd2
				else:
					res = opd1 / opd2
			elif opt == ">":
				res = opd1 > opd2
			elif opt == "<":
				res = opd1 < opd2
			elif opt == ">=":
				res = opd1 >= opd2
			elif opt == "<=":
				res = opd1 <= opd2
			elif opt == "==":
				res = opd1 == opd2
			elif opt == "!=":
				res = opd1 != opd2


			resDir = prepRes(res,resVar.varType)
			resVar.varVal = resDir
			print (num,"|",opd1,"|",opd2,"|",opt,"|",resVar.varDir,"\n")
			x = x +1
