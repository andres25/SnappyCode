from varGlobales import *
from procVarTables import *
from memory import *
import turtle
import copy

cuadEjec = 0
memEntero = 0
memFlotante = 0
memTexto = 0
memBooleano = 0

# grapgics turtle
turtle.setup(800, 600)
wn = turtle.Screen()
wn.title("SnappyCode")

#wn.exitonclick()

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

def getConsFromParam(cuadruplo):
	opdDir = cuadruplo.opd1

	isVar = True
	while isVar:
		if opdDir == None:
			return
		elif opdDir >= 0 and opdDir < 4000:
			for var in varGlb:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		elif opdDir >= 7000 and opdDir < 12000:
			for var in tempTable:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		elif opdDir >= 4000 and opdDir < 7000:
			lastVarSpace = pilaVarTableLocSpace.pop()
			for var in lastVarSpace:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
			pilaVarTableLocSpace.append(lastVarSpace)
		elif opdDir >= 12000 and opdDir < 16000:
			isVar = False
	return opdDir
	
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

	return None

def getVarFromDir(opdDir):
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

	return None

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
		elif cType == 'booleano':
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
	if not memEntero > 12000:
		memEntero = 12000;
	if not memFlotante > 13000:
		memFlotante = 13000;
	if not memTexto > 14000:
		memTexto = 14000;
	if not memBooleano > 15000:
		memBooleano = 15000;
def getCuadMain():
	for proc in procTable:
		if proc.procName == 'main':
			return proc.procDir

def getProcByJumpDir(jumpDir):
	for proc in procTable:
		if proc.procDir == jumpDir:
			return proc

def setParam(varDir, pName, numparam):
	paramsFunc = None
	procVars = None
	proc = getProc(pName)
	paramsFunc = proc.procParams.copy()
	procVars = proc.procVars
	paramsFunc[numparam].varVal = varDir
	procVars.append(paramsFunc[numparam])

def InterpretarCuadruplos():
	global tess
	x = getCuadMain()
	initMem()
	while x < len(cuadruplos):
		cuadruplos[x].printCuad()
		opt = cuadruplos[x].opt
		num = cuadruplos[x].num
		if opt == 'GOTO':
			x = cuadruplos[x].opd2
		elif opt == 'GOTOF':
			val = getOperand(cuadruplos[x], 1)
			if val == 0:
				x = cuadruplos[x].opd2
			else:
				x = x + 1
		elif opt == 'ERA':
			procName = cuadruplos[x].opd2
			proc = getProc(procName)
			auxVarTable = proc.procVars.copy()
			pilaVarTableLocSpace.append(auxVarTable)
			pilaVarTableLocSpaceName.append(proc.procName)
			procClean = getProcClean(procName)
			proc.procVars = procClean.procVars
			x = x + 1
		elif opt == 'GOSUB':
			procName = cuadruplos[x].opd2
			proc = getProc(procName)
			numParam = 0
			y = x + 1
			opt = cuadruplos[y].opt
			while opt == 'PARAM':
				cuadruplos[y].printCuad()
				opd = getConsFromParam(cuadruplos[y])
				setParam(opd,procName,numParam)
				numParam = numParam + 1
				y = y + 1
				opt = cuadruplos[y].opt
			pilaSaltosEjec.append(y)
			x = proc.procDir
			print('Tabla Intermedia de Variables', '\n')
			for var in proc.procVars:
				print ("    " + var.varName, " - ", var.varVal, " - ",var.varType, " - ", var.varDir, "-", var.varDim)
		elif opt == 'ENDPROC':
			x = pilaSaltosEjec.pop()
			procName = pilaVarTableLocSpaceName.pop()
			proc = getProc(procName)
			auxVarTable = pilaVarTableLocSpace.pop()
			proc.procVars = auxVarTable
		elif opt == 'ENDPROG':
			turtle.exitonclick()
			x = x+1
		elif opt == 'PRINT':
			opd1 = getOperand(cuadruplos[x], 1)
			print (opd1)
			x = x + 1

		elif opt == 'VER':
			index = getOperand(cuadruplos[x], 1)
			limS = cuadruplos[x].res
			if (index>=limS or index<0):
				print ("Indice fuera del rango del arreglo")
				sys.exit()
			x = x + 1
		elif opt == 'OFST':
			index = getOperand(cuadruplos[x], 1)
			arrayDir = cuadruplos[x].opd2
			resVar = getResult(cuadruplos[x])
			res = index + arrayDir
			resDir = prepRes(res,resVar.varType)
			resVar.varVal = resDir
			x = x + 1
		elif opt == 'ARYAS':
			opdDir = cuadruplos[x].opd1
			print (opdDir)
			resVar = getResult(cuadruplos[x])
			for cons in consTable:
				if cons.consDir == resVar.varVal:
					realDir = cons.consVal
			arrDir = getVarFromDir(realDir)
			#No se ha asigando el index del arreglo
			if (arrDir == None):
				opdVal = getOperand(cuadruplos[x], 2)
				baseArray = getVarFromDir(realDir - opdVal)
				print(realDir)
				if realDir >= 0 and realDir < 4000:
					#global
					varGlbInsert(realDir, opdDir, baseArray.varType, realDir)
					print (realDir,"|",opdDir,"|",baseArray.varType,"|",realDir,"\n")
				elif realDir >= 4000 and realDir < 7000:
					#procTable
					for proc in procTable:
						for var in proc.procVars:
							if var.varDir == arrayDir.varDir:
								arrProc = proc.Name
					varLocInsert(realDir, opdDir, baseArray.varType, realDir, arrProc)
					print (realDir,"|",opdDir,"|",baseArray.varType,"|",realDir,"|",arrProc,"\n")
			#Ya existe el index del arreglo
			else:
				print('cero')
				print(opdDir)
				arrDir.varVal = opdDir
			x = x + 1
		elif opt == 'MOVER':
			turtle.forward(getOperand(cuadruplos[x], 1))
			x = x+1
		elif opt == 'PINTAR':
			turtle.pendown()
			x = x+1
		elif opt == 'DESPINTAR':
			turtle.penup()
			x = x+1
		elif opt == 'BORRAR':
			turtle.reset()
			x = x+1
		elif opt == 'GIRARDERECHA':
			turtle.right(getOperand(cuadruplos[x], 1))
			x = x+1
		elif opt == 'GIRARIZQUIERDA':
			turtle.left(getOperand(cuadruplos[x], 1))
			x = x+1
		elif opt == '=':
			opdDir = cuadruplos[x].opd1
			resVar = getResult(cuadruplos[x])
			resVar.varVal = opdDir
			#print (num,"|",opdDir,"|",None,"|",opt,"|",resVar.varDir,"\n")
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
			x = x +1
		