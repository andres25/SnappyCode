from varGlobales import *
from procVarTables import *
from memory import *
import turtle
import copy

#Inicializacion de varaibles globales utilizadas en interpretacion de codigo
cuadEjec = 0
memEntero = 0
memFlotante = 0
memTexto = 0
memBooleano = 0

# grapgics turtle
turtle.setup(800, 600)
turtle.speed('normal')
wn = turtle.Screen()
wn.title("SnappyCode")

#Pilas utilizadas para el almacenamiento y reinstauracion de espacios de memoria en llamadas a funcion
pilaSaltosEjec = []
pilaVarTableLocSpace = []
pilaVarTableLocSpaceName = []

# getOperand
#
# Obtiene el valor guardado en una constante, dada una direccion de memoria dentro de un cuadruplo
#
# @param cuadruplo es el objeto de tipo <code>cuadruplo</code> que se genero en compilacion
# @param num es un numero de tipo <code>integer</code> que indica a que parte del cuadruplo accesar
#	1 = Operando 1
#	2 = Operando 2
#	3 = Resultado
# @return el valor almacenado en un objeto de tipo <code>consTableNode</code> 

def getOperand(cuadruplo, num):
	#Se evalua el parametro num, obteniendo la direccion de memoria de la parte del cuadruplo
	#correspondiente
	if (num == 1):
		opdDir = cuadruplo.opd1
	elif (num == 2):
		opdDir = cuadruplo.opd2
	elif (num == 3):
		opdDir = cuadruplo.res

	if opdDir == None:
		return

	#Se inicia con la premisa de que la direccion obtenida pertenece a una variable
	isVar = True
	while isVar:
		#Se evalua si la direccion pertene a variables globales
		if opdDir >= 0 and opdDir < 4000:
			#Se busca en la tabla de variables globales
			for var in varGlb:
				#Si se llega a encontrar, opdDir toma el valor de la direccion a la
				#cual apunta la variable global
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
			if num == 3:
				return None
		#Se evalua si la direccion pertene a variables locales
		elif opdDir >= 4000 and opdDir < 8000:
			#Se busca en la tabla de variables locales de cada proceddimiento
			for proc in procTable:
				for var in proc.procVars:
					#Si se llega a encontrar, opdDir toma el valor de la direccion a la
					#cual apunta la variable local
					if var.varDir == opdDir:
						opdVar = var
						opdDir = var.varVal
			if num == 3:
				return None
		#Se evalua si la direccion pertene a variables temporales
		elif opdDir >= 8000 and opdDir < 12000:
			#Se busca en la tabla de variables temporales
			for var in tempTable:
				#Si se llega a encontrar, opdDir toma el valor de la direccion a la
				#cual apunta la variable temporal
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
			if num == 3:
				return None
		#Se evalua si la direccion pertene a constantes, si es asi entonces ya no es
		#una variable y se sale del ciclo
		elif opdDir >= 12000 and opdDir < 16000:
			isVar = False
	#Una vez fuera del ciclo se busca la constante y se regresa el valor guardado en
	#en ella
	for cons in consTable:
		if cons.consDir == opdDir:
			return cons.consVal

# getConsFromParam
#
# Obtiene la direccion de la constante de un parametro
#
# @param cuadruplo es el objeto de tipo <code>cuadruplo</code> que se genero en compilacion
# @return la direccion de la constante de un parametro de tipo <code>varTableNode</code> 

def getConsFromParam(cuadruplo):
	#Se obteniene la direccion de memoria de la primera parte del cuadruplo
	opdDir = cuadruplo.opd1
	#Se inicia con la premisa de que la direccion obtenida pertenece a una variable
	isVar = True
	while isVar:
		if opdDir == None:
			return
		#Se evalua si la direccion pertene a variables globales
		elif opdDir >= 0 and opdDir < 4000:
			for var in varGlb:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		#Se evalua si la direccion pertene a variables temporales
		elif opdDir >= 8000 and opdDir < 12000:
			for var in tempTable:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		#Se evalua si la direccion pertene a variables locales
		elif opdDir >= 4000 and opdDir < 8000:
			#Se obtiene el espacio de memoria del cual se realizo la llamad a a la funcion
			lastVarSpace = pilaVarTableLocSpace[-1]
			for var in lastVarSpace:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		#Se evalua si la direccion pertene a constantes, si es asi entonces ya no es
		#una variable y se sale del ciclo
		elif opdDir >= 12000 and opdDir < 16000:
			isVar = False
	#Se regresa la direccion de la constante encontrada
	return opdDir

# getConsFromVar
#
# Obtiene la direccion de la constante de una variable
#
# @param var de tipo  <code>varTableNode</code> 
# @return la direccion de la constante a la que apunta una variable de tipo
# <code>varTableNode</code> 

def getConsFromVar(var):
	#Se obtiene la direccion de la variable
	opdDir = var.varDir

	#Se inicia con la premisa de que la direccion obtenida pertenece a una variable
	isVar = True
	while isVar:
		#Se evalua si la direccion pertene a variables globales
		if opdDir >= 0 and opdDir < 4000:
			for var in varGlb:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		#Se evalua si la direccion pertene a variables locales
		elif opdDir >= 4000 and opdDir < 8000:
			for proc in procTable:
				for var in proc.procVars:
					if var.varDir == opdDir:
						opdVar = var
						opdDir = var.varVal
		#Se evalua si la direccion pertene a variables temporales
		elif opdDir >= 8000 and opdDir < 12000:
			for var in tempTable:
				if var.varDir == opdDir:
					opdVar = var
					opdDir = var.varVal
		#Se evalua si la direccion pertene a constantes, si es asi entonces ya no es
		#una variable y se sale del ciclo
		elif opdDir >= 12000 and opdDir < 16000:
			isVar = False
	#Una vez fuera del ciclo se busca la constante y se regresa el valor guardado en
	#en ella
	for cons in consTable:
		if cons.consDir == opdDir:
			return cons

# getResult
#
# Obtiene la variable de la cuarta parte de un cuadruplo
#
# @param cuadruplo es el objeto de tipo <code>cuadruplo</code> que se genero en compilacion
# @return el objeto de tipo <code>varTableNode</code> referenciado por la direccion de la 
# cuarta parte de un cuadruplo
	
def getResult(cuadruplo):
	opdDir = cuadruplo.res
	if opdDir == None:
		return
	#Se evalua si la direccion pertene a variables globales
	elif opdDir >= 0 and opdDir < 4000:
		for var in varGlb:
			if var.varDir == opdDir:
				return var
	#Se evalua si la direccion pertene a variables locales
	elif opdDir >= 4000 and opdDir < 8000:
		for proc in procTable:
			for var in proc.procVars:
				if var.varDir == opdDir:
					return var
	#Se evalua si la direccion pertene a variables temporales
	elif opdDir >= 8000 and opdDir < 12000:
		for var in tempTable:
			if var.varDir == opdDir:
				return var

	return None


# getVarFromDir
#
# Obtiene la variable referenciada por una direccion de memoria
#
# @param opdDir es el objeto de tipo <code>intger</code> el cual es una direccion de memoria
# que puede hacer referencia a una variable
# @return el objeto de tipo <code>varTableNode</code> referenciado por la direccion ingresada
# como parametro
def getVarFromDir(opdDir):
	if opdDir == None:
		return
	#Se evalua si la direccion pertene a variables globales
	elif opdDir >= 0 and opdDir < 4000:
		for var in varGlb:
			if var.varDir == opdDir:
				return var
	#Se evalua si la direccion pertene a variables locales
	elif opdDir >= 4000 and opdDir < 8000:
		for proc in procTable:
			for var in proc.procVars:
				if var.varDir == opdDir:
					return var
	#Se evalua si la direccion pertene a variables temporales
	elif opdDir >= 8000 and opdDir < 12000:
		for var in tempTable:
			if var.varDir == opdDir:
				return var
	#Se evalua si la direccion pertene a una constante
	elif opdDir >= 12000 and opdDir < 16000:
		for cons in consTable:
			if cons.consDir == opdDir:
				return cons

	return None

# prepRes
#
# Evalua si un valor se encuentra en la tabla de constante y si no, lo inserta y regresa
# la direccion de dicho valor
#
# @param cVal puede ser un objeto de tipo <code>integer</code>, <code>string</code>, 
# <code>float</code> o <code>boolean</code>
# @param cType es un texto de tipo <code>stirng</code> que contiene el tipo de cVal
# @return la direccion de memoria que hace referencia a cVal

def prepRes(cVal, cType):
	global memEntero
	global memFlotante
	global memTexto
	global memBooleano
	#Se busca la direcccion de memoria de cVal
	consDir = consGetDir(cVal)
	#En caso de ser igual a None significa que no se encontro
	if consDir == None:
		#Se inserta en la tabla de constantes con su respectiva asignacion de memoria
		#dependiendo del tipo
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
		#Se regresa la direccion de memoria
		return mem
	else:
		#Se regresa la direccion de memoria
		return consDir
	
	
# initMem
#
# Inicializa los valores de memoria para las constantante s de los diversos tipos
# de acuerdo a como terminar en compilacion

# @param
# @return

def initMem():
	global memEntero
	global memFlotante
	global memTexto
	global memBooleano
	#Se obtiene la direccion mayor para cada tipo de memoria
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

	#Si no cambio el valor entonces se inicializa
	if not memEntero > 12000:
		memEntero = 12000;
	if not memFlotante > 13000:
		memFlotante = 13000;
	if not memTexto > 14000:
		memTexto = 14000;
	if not memBooleano > 15000:
		memBooleano = 15000;
	consInsert(None, None, 15999)

# getCuadMain
#
# Obtiene el cuadruplo donde empieza el bloque principal de ejecucion

# @param
# @return regresa el numero de cuadruplo de tipo <code>entero</code>
# donde empieza la ejecucion del bloque principal
def getCuadMain():
	for proc in procTable:
		if proc.procName == 'main':
			return proc.procDir

# getProcByJumpDir
#
# Obtiene un procedimiento en base a la direccion del cuadruplo donde empieza
# su ejecucion

# @param numero de tipo <code>entero</code> que indica el numero de cuadruplo
# donde empieza la ejecucion de un procedimiento
# @return regresa el procedimiento que coincide con el numero de cuadruplo
# recibido
def getProcByJumpDir(jumpDir):
	for proc in procTable:
		if proc.procDir == jumpDir:
			return proc



# setParam
#
# Inserta una variabe en el procedimiento destino

# @param consDir de tipo <code>entero</code> que indica la direccion de la constante
# con la cual se inicializara el parametro
# @param pName de tipo <code>string</code> que indica el nombre del procedimiento
# donde se insertara la variable
# @param numparam de tipo <code>entero</code> que indica el numero de parametro 
# a insertar
# @return 
def setParam(consDir, pName, numparam):
	paramsFunc = None
	procVars = None
	#Obtiene el procedimietno en base al nombre
	proc = getProc(pName)
	#Realiza una copia de los parametros del procedimiento
	paramsFunc = proc.procParams.copy()
	#Obtiene la tabla de variables del procedimiento
	procVars = proc.procVars
	#Obtiene el parametro dependiendo del numero proporcionado
	# y lo inicializa con el valor de la constante proporcionada
	paramsFunc[numparam].varVal = consDir
	#Agrega el parametro a la tabla de variables del procedimiento
	procVars.append(paramsFunc[numparam])


# InterpretarCuadruplos
#
# Metodo llamaod una vez terminada la compilacion donde se realiza la interpretacion
# de cuadruplos
# @param 
# @return 
def InterpretarCuadruplos():
	#Se obtiene el cuadruplo donde inicia el bloque principal
	x = getCuadMain()
	#Se inicializa la memoria de las constantes en base al resultado de compilacion
	initMem()
	#Se ejecuta un ciclio mientras se llegue al final de los cuadruplos
	while x < len(cuadruplos):
		#cuadruplos[x].printCuad()
		#Se obtiene el operador del cuadruplo
		opt = cuadruplos[x].opt
		#Empieza un estatuto condicional if en el cual se realizan acciones especificas
		#dependiendo del operador del cuadruplo que esta siendo interpretado
		if opt == 'GOTO':
			#La variable de ejecucion toma el valor indicado en el cuadruplo
			x = cuadruplos[x].opd2
		elif opt == 'GOTOF':
			#Se obtiene el valor indicado en el cuadruplo para la evaluacion
			val = getOperand(cuadruplos[x], 1)
			#Se realiza el salto si el valor es False
			if val == 0:
				#La variable de ejecucion toma el valor indicado en el cuadruplo
				x = cuadruplos[x].opd2
			else:
				#Se procede con el siguiente cuadruplo
				x = x + 1
		elif opt == 'ERA':
			#Si esta vacia, significa que la llamada es desde main
			#Por lo tanto se inserta main en la pila
			if len(pilaVarTableLocSpaceName) == 0:
				#Se inserta el nombre del proc actual
				pilaVarTableLocSpaceName.append('main')


			#Se resplada el proc actual
			procOrigenName = pilaVarTableLocSpaceName[-1]
			procOrigen = getProc(procOrigenName)
			auxVarTable = copy.deepcopy(procOrigen.procVars)
			pilaVarTableLocSpace.append(auxVarTable)

			#Se obtiene el proc Destino
			procDestinoName = cuadruplos[x].opd2
			procDestino = getProc(procDestinoName)

			#Se limpia el proc Destino
			procClean = getProcClean(procDestinoName)
			procDestino.procVars = procClean.procVars

			#Se inserta el nombre del nuevo proc actual
			pilaVarTableLocSpaceName.append(procDestinoName)

			#Se procede con el siguiente cuadruplo
			x = x + 1
		elif opt == 'GOSUB':
			#Se obtiene el nombre del procedimiento indicado en el cuadruplo
			procName = cuadruplos[x].opd2
			#Se obtiene el procedimiento en base al nombre
			proc = getProc(procName)
			#Se inicializa el parametro procesado en 0
			numParam = 0
			#Se obsera el cuadruplo siguiente
			y = x + 1
			opt = cuadruplos[y].opt
			#Si el cuaruplo siguiente es un parametro entonces se inserta en el procedimiento
			#destino
			while opt == 'PARAM':
				#cuadruplos[y].printCuad()
				opd = getConsFromParam(cuadruplos[y])
				setParam(opd,procName,numParam)
				numParam = numParam + 1
				y = y + 1
				opt = cuadruplos[y].opt
			#Se guarda en una pila el cuadruplo de ejecucion en el cual se quedo la interpretacion
			#antes de la llamada a funcion
			pilaSaltosEjec.append(y)
			#Se realiza el salto a la funcion
			x = proc.procDir
		elif opt == 'ENDPROC':
			#Se regresa al ultimo cuadruplo contenido en pila de ejecucion
			x = pilaSaltosEjec.pop()

			#Remover proc Actual de la pila porque se acaba su ejecucion
			procAnteriorName = pilaVarTableLocSpaceName.pop()
			procAnterior = getProc(procAnteriorName)


			#Obtener el proc actual
			procName = pilaVarTableLocSpaceName[-1]
			proc = getProc(procName)


			#Obtener el espacio de memoria para el proc almacenado antes de la 
			#ultima llamada a funcion
			auxVarTable = pilaVarTableLocSpace.pop()

			#Guardar el valor obtenido al terminar la ejecucion de la funcion
			returnVar = procAnterior.procRetVar
			varDir = None
			for var in procAnterior.procVars:
				if var.varDir == returnVar.varVal:
					cons = getConsFromVar(var)
					consDir = cons.consDir
					varDir = var.varDir


			#Regresar el espacio de memoria antes de la llamada
			proc.procVars = auxVarTable

			
			#Actualizar con el valor obtenido al terminar la ejecucion de la funcion
			if varDir:
				for var in proc.procVars:
					if var.varDir == varDir:
						var.varVal = consDir

		
		elif opt == 'ENDPROG':
			#Cuando se da click a la pantalla se cierra
			turtle.exitonclick()
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == 'VER':
			#Verifica que el index recibido en el cuadruplo se encuentre 
			#dentro del rango aceptado para un arreglo, de lo contrario informa
			#al usuario
			index = getOperand(cuadruplos[x], 1)
			limS = cuadruplos[x].res
			if (index>limS or index<0):
				print ("Indice fuera del rango del arreglo")
				sys.exit()
			x = x + 1
		elif opt == 'OFST':
			#Calcula la direccion de memoria de un arreglo en base a su indice
			#y regresa dicha direccon en un temporal
			index = getOperand(cuadruplos[x], 1)
			arrayDir = cuadruplos[x].opd2
			resVar = getResult(cuadruplos[x])
			res = index + arrayDir
			resDir = prepRes(res,resVar.varType)
			resVar.varVal = resDir
			#Se procede con el siguiente cuadruplo
			x = x + 1
		elif opt == 'ARYAS':
			#Asignacion de un valor para un arreglo
			#Se obtiene la direccion a asignar indicada en el cuadruplo
			opdDir = cuadruplos[x].opd1
			#En caso de tratarse de una variable o un temporal se obtiene la constante
			#a la cual apuntan
			if opdDir >= 0 and opdDir < 12000:
				opdTemp = getVarFromDir(opdDir)
				opdDir = opdTemp.varVal
			#Se obtiene el index
			indexVal = getOperand(cuadruplos[x], 2)
			#Se obtiene la direccion de la constante que contiene la direccion del arreglo
			newArrayDir = getVarFromDir(cuadruplos[x].res).varVal
			#Se obtiene la direccion del arreglo almacenado en la constante
			newArrayVal = getVarFromDir(newArrayDir).consVal 
			#Se calcula direccion del arreglo base restanto el indice
			baseArray = getVarFromDir(newArrayVal - indexVal)
			#Si el arreglo base es global realiza lo siguiente:
			if baseArray.varDir >= 0 and baseArray.varDir < 4000:
				#Inserta o actualiza la variable en la tabla de variables globales
				if indexVal == 0:
					varName = str(baseArray.varName)
				else:
					varName = str(baseArray.varName)+'['+str(indexVal)+']'
				varGlbInsert(varName, opdDir, baseArray.varType, newArrayVal,None,1)
			#El arreglo base es local y realiza lo siguiente:
			elif baseArray.varDir >= 4000 and baseArray.varDir < 8000:
				#Inserta o actualiza la variable en su respectiva tabla de variables locales
				for proc in procTable:
					for var in proc.procVars:
						if var.varDir == baseArray.varDir:
							arrProc = proc.procName
				if indexVal == 0:
					varName = str(baseArray.varName)
				else:
					varName = str(baseArray.varName)+'['+str(indexVal)+']'
				varLocInsert(varName, opdDir, baseArray.varType, newArrayVal, arrProc,None,1)
			#Se procede con el siguiente cuadruplo
			x = x + 1
		elif opt == 'ARYCA':
			#Se ejecuta lo siguiente cuando se intenta accessar a un arreglo
			#Se obtiene el index
			index = getOperand(cuadruplos[x], 1)
			#Se obtiene la direccion base del arreglo
			baseArrDir = cuadruplos[x].opd2
			#Se obtiene el resultado
			resVar = getResult(cuadruplos[x])
			#Se obtiene la direccion del arreglo
			arrDir = index + baseArrDir
			#Se busca el arreglo en la tabla de variables
			arr = getVarFromDir(arrDir)

			if arr:
				#Si se encontro entonces se le asigna el valor de dicha variable
				#al resultado
				resVar.varVal = arr.varVal
			else:
				#Si no se encontro se le asigna el valor de None de la tabla de 
				#constantes
				resVar.varVal = 15999
			#Se procede con el siguiente cuadruplo
			x = x + 1
		elif opt == 'PRINT':
			#Se obtiene el operando
			opd1 = getOperand(cuadruplos[x], 1)
			#Se realiza la accion de desplegar en pantalla
			print (opd1)
			#Se procede con el siguiente cuadruplo
			x = x + 1
		elif opt == 'INPUT':
			#Se obtiene la variable donde se guardara el resultado
			result = getResult(cuadruplos[x])
			inputVal = input('Input:')
			#Se obtiene el tipo de la variable que se espera el usuario ingrese
			inputType  = cuadruplos[x].opd1
			#Se castea a su respectivo tipo lo que el usuario haya ingresado
			if (inputType == 'entero'):
				inputVal = int(inputVal)
			elif (inputType == 'flotante'):
				inputVal = float(inputVal)
			elif (inputType == 'booleano'):
				inputval = bool(inputVal)
			#Se realiza la asignacion a la variable proporcionada
			resDir = prepRes(inputVal,inputType)
			result.varVal = resDir
			#Se procede con el siguiente cuadruplo
			x = x + 1
		elif opt == 'MOVER':
			#Se mueve la flecha dependiendo del valor referenciado por la direccion
			#de memoria indicada en el cuadruplo
			turtle.forward(getOperand(cuadruplos[x], 1))
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == 'RETROCEDE':
			#Se mueve en sentido inverso la flecha dependiendo del valor referenciado 
			#por la direccion de memoria indicada en el cuadruplo
			turtle.backward(getOperand(cuadruplos[x], 1))
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == 'PINTAR':
			#Se inicializa la escritura para los movimiento de la flecha
			turtle.pendown()
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == 'DESPINTAR':
			#Se detiene la escritura para los movimientos de la flecha
			turtle.penup()
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == 'BORRAR':
			#Se limpia la pantalla
			turtle.reset()
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == 'GIRARDERECHA':
			#Gira hacia la derecha cierta cantidad de grados contenidos en el valor 
			#referenciado por la direccion de memoria indicada en el cuadruplo
			turtle.right(getOperand(cuadruplos[x], 1))
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == 'GIRARIZQUIERDA':
			#Gira hacia la izquierda cierta cantidad de grados contenidos en el valor 
			#referenciado por la direccion de memoria indicada en el cuadruplo
			turtle.left(getOperand(cuadruplos[x], 1))
			#Se procede con el siguiente cuadruplo
			x = x+1
		elif opt == '=':

			#Asignacion de un valor para una variable
			#Se obtiene la direccion a asignar indicada en el cuadruplo
			opdDir = cuadruplos[x].opd1
			#En caso de tratarse de una variable o un temporal se obtiene la constante
			#a la cual apuntan
			if opdDir >= 0 and opdDir < 12000:
				var = getVarFromDir(opdDir)
				cons = getConsFromVar(var)
				opdDir = cons.consDir
			#Actualiza la variable en indicada en la ultima parte del cuadruplo
			resVar = getResult(cuadruplos[x])
			resVar.varVal = opdDir
			#Se procede con el siguiente cuadruplo
			x = x+1
		else:
			#Se obtiene los operandos y el resultado para realizar operaciones aritmeticas
			opd1 = getOperand(cuadruplos[x], 1)
			opd2 = getOperand(cuadruplos[x], 2)
			resVar = getResult(cuadruplos[x])

			#Se realizan las operaciones y se guarda el resultado
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
			elif opt == "&&":
				res = opd1 and opd2
			elif opt == "||":
				res = opd1 or opd2

			#Se obtiene la direccion del resultado en la tabla de constantes
			resDir = prepRes(res,resVar.varType)
			#Se realiza la actualizacion a la variable indicada en la ultima parte
			#del cuadruplo
			resVar.varVal = resDir
			x = x +1
		