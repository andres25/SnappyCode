#----------------------------------------------
# procVarTables.py
# ProcTable & VarTable
# Manuel Calzado Maycotte A00811102
# Juan Paulo Lara Rodriguez A00999823
# CREADO: 18/03/2014
#----------------------------------------------
from varGlobales import *
import sys
import copy

class varTableNode:
	def __init__(self, vName, vVal, vType, vDir, vDim = None):
		self.varName= vName
		self.varVal= vVal
		self.varType = vType
		self.varDir = vDir
		self.varDim = vDim

class procTableNode:
	def __init__(self, pName, pType, pDir, pRetVar):
		self.procName = pName
		self.procReturn = pType
		self.procRetVar = pRetVar
		self.procDir = pDir
		self.procVars= []
		self.procParams =  []
		self.procUsed = False

class consTableNode:
	def __init__(self, cVal, cType, cDir):
		self.consVal= cVal
		self.consType = cType
		self.consDir = cDir

def procInsert(pName, pType, pDir, pRetVar=None):
	global procTable
	if procFind(pName):
		print("Error Semantico: Procedimiento ", pName, " ya fue declarado")
		sys.exit()
	else:
		node = procTableNode(pName, pType, pDir, pRetVar)
		procTable.append(node)


def varLocInsert(vName, vVal, vType, vDir, pName, vDim = None, vEdit=None):
	global procTable
	for proc in procTable:
		if proc.procName == pName:
			if varFind(proc.procVars,vName):
				if vEdit != None:
					var = getVar(proc.procVars,vName)
					var.varVal =vVal
				else:
					print("Error Semantico: Variable ", vName, " ya fue declarada")
					sys.exit()
			else:
				var = varTableNode(vName, vVal, vType, vDir, vDim)
				proc.procVars.append(var)

def paramInsert(vName, vType, vDir, pName):
	global procTable
	var = varTableNode(vName, None, vType, vDir)
	for proc in procTable:
		if proc.procName == pName:
			proc.procParams.append(var)

def varGlbInsert(vName, vVal, vType, vDir, vDim = None, vEdit=None):
	global varGlb

	if varFind(varGlb,vName):
		if vEdit != None:
			var = getVar(varGlb,vName)
			var.varVal =vVal
		else:
			print("Error Semantico: Variable ", vName, " ya fue declarada")
			sys.exit()
	else:
		var = varTableNode(vName, vVal, vType, vDir, vDim)
		varGlb.append(var)

def procFind(pName):
	global procTable
	for proc in procTable:
		if proc.procName == pName:
			return True
	return False

def getProc(pName):
	global procTable
	for proc in procTable:
		if proc.procName == pName:
			return proc

def getProcClean(pName):
	global procTableClean
	for proc in procTableClean[0]:
		if proc.procName == pName:
			return copy.deepcopy(proc)

def getVarTable(pName):
	global procTable
	for proc in procTable:
		if proc.procName == pName:
			return proc.procVars

def varFind(varTable, vName):
	for var in varTable:
		if var.varName == vName:
			return True
	return False

def getVar(varTable, vName):
	for var in varTable:
		if var.varName == vName:
			return var

def procPrint(procTable):
	global varGlb
	print ("Tabla de procedimientos y variables")
	for proc in procTable:
		if proc:
			retVar = proc.procRetVar
			if proc.procName != 'main':
				print (proc.procName, " - ", proc.procReturn, " - ", proc.procDir,  " - ", retVar.varDir)
			else:
				print (proc.procName, " - ", proc.procReturn, " - ", proc.procDir)
			print ("  Params")
			for param in proc.procParams:
				print ("    " + param.varName, " - ", param.varType, " - ", param.varDir)
			print ("\n")
			print ("  Vars")
			for var in proc.procVars:
				print ("    " + var.varName, " - ", var.varVal, " - ",var.varType, " - ", var.varDir, "-", var.varDim)
			print ("\n")
		else:
			print ("No procs defined")
			print ("\n")
	print ("Tabla de variables globales")
	for var in varGlb:
		if var:
			print (var.varName," - ", var.varVal," - ",var.varType, " - ",var.varDir, "-", var.varDim)
		else:
			print ("ConsTable is empty")
	print ("\n")
	print ("Tabla de constantes")
	for cons in consTable:
		if cons:
			print (cons.consVal," - ", cons.consType, " - ",cons.consDir)
		else:
			print ("ConsTable is empty")
	print ("\n")
	print ("Tabla de temporales")
	for temp in tempTable:
		if temp:
			print (temp.varName," - ", temp.varVal," - ", temp.varType, " - ",temp.varDir)
		else:
			print ("TempTable is empty")
	print ("\n")

def consInsert(cVal, cType, cDir):
	global consTable
	if consGetDir(cVal) == None:
		cons = consTableNode(cVal, cType, cDir)
		consTable.append(cons)
		return True
	return False
	
	

def consGetVal(cDir):
	global consTable
	for cons in consTable:
		if cons.consDir == cDir:
			return cons.cVal


def consGetDir(cVal):
	global consTable
	for cons in consTable:
		if cons.consVal == cVal:
			return cons.consDir

def tempInsert(tVar):
	global tempTable
	tempTable.append(tVar)

def getType(value):
	if type(value) is int:
		return "entero"
	elif type(value) is float:
		return "flotante"
	elif type(value) is bool:
		return "booleano"
	else:
		return "texto"