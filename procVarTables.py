#----------------------------------------------
# procVarTables.py
# ProcTable & VarTable
# Manuel Calzado Maycotte A00811102
# Juan Paulo Lara Rodriguez A00999823
# CREADO: 18/03/2014
#----------------------------------------------

import sys

class varTableNode:
	def __init__(self, vName, vType, vDir):
		self.varName= vName
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

procTable = [ ]
varGlb = [ ]

def procInsert(pName, pType, pDir):
	global procTable
	node = procTableNode(pName, pType, pDir)
	procTable.append(node)


def varLocInsert(vName, vType, vDir, pName):
	global procTable
	var = varTableNode(vName, vType, vDir)
	for proc in procTable:
		if proc.procName == pName:
			proc.procVars.append(var)

def paramInsert(vName, vType, vDir, pName):
	global procTable
	var = varTableNode(vName, vType, vDir)
	for proc in procTable:
		if proc.procName == pName:
			proc.procParams.append(var)

def varGlbInsert(vName, vType, vDir):
	global varGlb
	var = varTableNode(vName, vType, vDir)
	varGlb.append(var)

def procFind(pName):
	global procTable
	for proc in procTable:
		if proc.procName == pName:
			sys.exit()

def varFind(varTable, vName):
	for var in varTable:
		if var.varName == vName:
			sys.exit()

def existe_var_asignar(varTable, vName):
	if not varFind(varTable, vName):
		print ("Error: " + vName + " no existe")
		sys.exit()


def procPrint(procTable):
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
				print ("    " + var.varName, " - ", var.varType, " - ", var.varDir)
			print ("\n")

		else:
			print ("No procs defined")