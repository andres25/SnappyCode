#----------------------------------------------
# procVarTables.py
# ProcTable & VarTable
# Manuel Calzado Maycotte A00811102
# Juan Paulo Lara Rodriguez A00999823
# CREADO: 18/03/2014
#----------------------------------------------

import sys

class varTableNode:
	def __init__(self, vName, vVal, vType, vDir):
		self.varName= vName
		self.varVal= vVal
		self.varType = vType
		self.varDir = vDir

class procTableNode:
	def __init__(self, pName, pType, pDir):
		self.procName = pName
		self.procReturn = pType
		self.procDir = pDir
		self.procVars= []
		self.procParams =  []
		self.procUsed = False

class consTableNode:
	def __init__(self, cVal, cType, cDir):
		self.consVal= cVal
		self.consType = cType
		self.consDir = cDir

consTable = [ ]
procTable = [ ]
varGlb = [ ]

def procInsert(pName, pType, pDir):
	global procTable
	node = procTableNode(pName, pType, pDir)
	procTable.append(node)


def varLocInsert(vName, vVal, vType, vDir, pName):
	global procTable
	var = varTableNode(vName, vVal, vType, vDir)
	for proc in procTable:
		if proc.procName == pName:
			proc.procVars.append(var)

def paramInsert(vName, vType, vDir, pName):
	global procTable
	var = varTableNode(vName, None, vType, vDir)
	for proc in procTable:
		if proc.procName == pName:
			proc.procParams.append(var)

def varGlbInsert(vName, vVal, vType, vDir):
	global varGlb
	var = varTableNode(vName, vVal, vType, vDir)
	varGlb.append(var)

def procFind(pName):
	global procTable
	for proc in procTable:
		if proc.procName == pName:
			return True
	return False

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
			print (proc.procName, " - ", proc.procReturn, " - ", proc.procDir)
			print ("  Params")
			for param in proc.procParams:
				print ("    " + param.varName, " - ", param.varType, " - ", param.varDir)
			print ("\n")
			print ("  Vars")
			for var in proc.procVars:
				print ("    " + var.varName, " - ", var.varVal, " - ",var.varType, " - ", var.varDir)
			print ("\n")
		else:
			print ("No procs defined")
			print ("\n")
	print ("Tabla de variables globales")
	for var in varGlb:
		if var:
			print (var.varName," - ", var.varType, " - ",var.varDir)
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

def consInsert(cVal, cType, cDir):
	global consTable
	cons = consTableNode(cVal, cType, cDir)
	consTable.append(cons)
	
	

def consGetVal(cDir):
	global consTable
	for cons in consTable:
		if cons.cDir == cDir:
			return cons.cVal