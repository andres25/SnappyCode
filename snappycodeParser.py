# snappycodeParser.py

from ply.lex import TOKEN
import sys
import snappycodeLex
import fileinput
from cuadruplo import *
from procVarTables import *
from memory import *
from cubosemantico import *
from varGlobales import *
import copy
import vm

tokens = snappycodeLex.tokens
actualProc = "global"
memoria = 0
pilaOperadores = []
pilaOperandos = []
tempCont = 0
cuadCont = 0 
pilaSaltos = []
pilaParams = []

precedence = (
    ('nonassoc', 'MAYORQUE', 'MENORQUE', 'DIFERENTEQUE', 'IGUALQUE', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','MULT','DIV'),
    ('right','UMINUS'),
    )



def p_program(t): 
    'program : INICIOPROGRAMA vars cuerpo FINPROGRAMA'
    global procTable
    global cuadruplos
    global procTableClean 
    procTableCleanAux = copy.deepcopy(procTable)
    procTableClean.append(procTableCleanAux)
    procPrint(procTable)
    print ("Cuadruplos")
    for cuad in cuadruplos:
        print(cuad.num, '|', cuad.opt, '|', cuad.opd1, '|', cuad.opd2, '|', cuad.res , '\n')
    print ("Cuadruplos De Ejecucion")
    vm.InterpretarCuadruplos()
    pass


def p_vars(t):
    'vars : vars tipo_var'
    pass

def p_tipo_var(t):
    '''tipo_var : single
                | array'''

def p_single(t): 
    'single : CREAR tipo ID PUNTOCOMA '
    global memoria
    if actualProc == 'global':
      memoria = asigna_memoria_global(t[2])
      varGlbInsert(t[3], None, t[2], memoria)
    else:
      memoria = asigna_memoria_local(t[2])
      varLocInsert(t[3], None, t[2], memoria, actualProc)
    pass

def p_array(t):
    'array : CREAR tipo ID CORCHETEIZQ CTEENTERO CORCHETEDER PUNTOCOMA'
    global memoria
    if actualProc == 'global':
      memoria = asigna_memoria_global(t[2], t[5])
      varGlbInsert(t[3], None, t[2], memoria, t[5])
    else:
      memoria = asigna_memoria_local(t[2], t[5])
      varLocInsert(t[3], None, t[2], memoria, actualProc, t[5])
    memoria += t[5]
    pass

def p_tipo(t):
    '''tipo   : ENTERO
              | FLOTANTE
              | TEXTO
              | BOOLEANO'''
    t[0] = t[1]
    pass

def p_vars_empty(t): 
    'vars : empty'

def p_empty(t):
    'empty : '
    pass

 
def p_cuerpo(t): 
    'cuerpo : cuerpo_func principal'
    pass
 
def p_cuerpo_func(t): 
    '''cuerpo_func : cuerpo_func funcion 
         | empty'''
    pass
 
def p_funcion(t):
    'funcion : iniciofunc param vars finfunc'
    pass

def p_iniciofunc(t): 
    'iniciofunc : INICIOFUNCION tipo ID'
    global memoria
    global tempCont

    t[0]= t[3]
    global scope
    scope = 'parametro'
    global actualProc
    actualProc = t[3]
    procType= t[2]
    if procType == 'ENTERO':
      procType = 'entero'
    elif procType == 'FLOTANTE':
      procType = 'flotante'
    elif procType == 'TEXTO':
      procType = 'texto'
    elif procType == 'BOOLEANO':
      procType = 'booleano'
    elif procType == 'ENTERO':
      procType = 'entero'

    # Genera el temporal
    memoria = asigna_memoria_temporal(procType)
    operandoTemp = varTableNode('t'+str(tempCont), None, procType, memoria)
    tempInsert(operandoTemp)
    tempCont += 1

    procInsert(actualProc, procType, cuadCont, operandoTemp)

    pass

def p_param(t): 
    'param : PARAMETROS tipo ID param_mult'
    global scope
    scope = 'local'
    global memoria
      #params[t[3]] = {'type' : t[2]}
    memoria = asigna_memoria_local(t[2])
    paramInsert(t[3], t[2], memoria, actualProc)
    pass
     
 
def p_param_mult(t): 
    'param_mult : COMA tipo ID param_mult'
    global memoria
    memoria = asigna_memoria_local(t[2])
    paramInsert(t[3], t[2], memoria, actualProc)
    pass

def p_param_mult_empty(t): 
    'param_mult : empty'
    pass

def p_param_empty(t): 
    'param : empty'
    pass 


def p_finfunc(t): 
    'finfunc : C return FINFUNCION'
    global cuadCont
    global cuadruplos
    global procTable
    cuadruplo = Cuadruplo(cuadCont, 'ENDPROC',None , None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1
    returnVarOp = pilaOperandos.pop()
    proc = getProc(actualProc)
    returnVar = proc.procRetVar 
    if returnVarOp.varType != proc.procReturn:
      print ("Error Semantico: Valor de retorno incompatible con tipo de funcion ",proc.procReturn, " en ", actualProc )
      sys.exit()
    else:
      returnVar.varVal = returnVarOp.varDir
    pass

 
def p_C(t): 
    '''C : C estatuto 
           | empty'''
    pass
 
 
def p_estatuto(t): 
    '''estatuto : asignacion
           | condicion
           | ciclo
           | io
           | accion
           | llamada_sin_ret
           | return'''
    pass

def p_asignacion(t):
    'asignacion : ID asignacion_arreglo IGUAL expresion PUNTOCOMA'
    global varGlb
    global procTable
    global cuadCont
    global tempTable
    global tempCont

    if pilaOperandos:
      if varFind(varGlb,t[1]):
        auxVar = getVar(varGlb,t[1])
      else:
        proc = getProc(actualProc)
        auxParams = proc.procParams
        if varFind(auxParams, t[1]):
          auxVar = getVar(auxParams,t[1])
        else:
          auxTable = getVarTable(actualProc)
          if varFind(auxTable,t[1]):
            auxVar = getVar(auxTable,t[1])
          else:
            print ("Error Semantico: Variable ", t[1], " no encontrada para asignacion" )
            sys.exit()
      if t[2] == None:
        tempOperando = pilaOperandos.pop()
        resType = cubo_semantico[auxVar.varType][tempOperando.varType]['=']
        if resType != "error":
          cuadruplo = Cuadruplo(cuadCont, '=',tempOperando.varDir , None, auxVar.varDir)
          cuadruplos.append(cuadruplo)
          cuadCont += 1
        else:
          print ("Error Semantico: Variable ", auxVar.varType, " incompatible con valor ",t[4], " a asignar")
          sys.exit()
        pilaOperandos.append(auxVar)
      else:
        operando = pilaOperandos.pop()
        index = pilaOperandos.pop()
        resType = cubo_semantico[auxVar.varType][operando.varType]['=']
        if resType != "error" and index.varType == "entero":
          # Verifica el indice del arreglo
          cuadruplo = Cuadruplo(cuadCont, 'VER', index.varDir, 0, auxVar.varDim-1)
          cuadruplos.append(cuadruplo)
          cuadCont += 1
          # Genera el temporal
          memoria = asigna_memoria_temporal(resType)
          operandoTemp = varTableNode('t'+str(tempCont), None, resType, memoria)
          tempInsert(operandoTemp)
          tempCont += 1
          # Asigna al temporal la direccion del arreglo + el offset
          cuadruplo = Cuadruplo(cuadCont, 'OFST', index.varDir, auxVar.varDir, operandoTemp.varDir)
          cuadruplos.append(cuadruplo)
          cuadCont += 1
          # Asigna el valor al arreglo
          cuadruplo = Cuadruplo(cuadCont, 'ARYAS', operando.varDir, index.varDir, operandoTemp.varDir)
          cuadruplos.append(cuadruplo)
          cuadCont += 1
        else:
          print ("Error Semantico: Variable ", auxVar.varType, " incompatible con valor ",t[5], " a asignar")
          sys.exit()
        pilaOperandos.append(auxVar)
    pass

def p_asignacion_arreglo(t):
    'asignacion_arreglo : CORCHETEIZQ exp CORCHETEDER'
    t[0] = t[1]
    pass

def p_asignacion_arreglo_empty(t):
    'asignacion_arreglo : empty'
    pass

def p_expresion_eval(t): 
    '''expresion : exp MAYORQUE push_opt exp
           | exp MENORQUE push_opt exp
           | exp DIFERENTEQUE push_opt exp
           | exp IGUALQUE push_opt exp
           | exp MAYORIGUAL push_opt exp
           | exp MENORIGUAL push_opt exp'''
    global cuadruplos
    global pilaOperandos
    global pilaOperadores
    global memoria
    global tempCont
    global cuadCont
    
    if pilaOperadores:
      operador = pilaOperadores.pop()
      operando2 = pilaOperandos.pop()
      operando1 = pilaOperandos.pop()
      resType = cubo_semantico[operando1.varType][operando2.varType][operador]
      if resType != "error":
        memoria = asigna_memoria_temporal(resType)
        operandoTemp = varTableNode('t'+str(tempCont), None, resType, memoria)
        tempInsert(operandoTemp)
        tempCont += 1

        cuadruplo = Cuadruplo(cuadCont, operador, operando1.varDir, operando2.varDir, operandoTemp.varDir)
        cuadruplos.append(cuadruplo)
        cuadCont += 1

        pilaOperandos.append(operandoTemp)
        t[0]=t[1]
      else:
        print("Error Semantico: valores incompatibles en la comparacion")
        sys.exit()
    t[0]=t[1]
    pass

def p_exp_agrupacion(t): 
    'exp : PARENTIZQ expresion PARENTDER'
    t[0] = t[2]
    pass

def p_exp_binop(t):
    '''exp : exp MAS push_opt exp
           | exp MENOS push_opt exp
           | exp MULT push_opt exp
           | exp DIV push_opt exp'''
    global cuadruplos
    global pilaOperandos
    global pilaOperadores
    global memoria
    global tempCont
    global cuadCont
    
    if pilaOperadores:
      operador = pilaOperadores.pop()
      operando2 = pilaOperandos.pop()
      operando1 = pilaOperandos.pop()
      resType = cubo_semantico[operando1.varType][operando2.varType][operador]
      if resType != "error":
        memoria = asigna_memoria_temporal(resType)
        operandoTemp = varTableNode('t'+str(tempCont), None, resType, memoria)
        tempInsert(operandoTemp)
        tempCont += 1

        cuadruplo = Cuadruplo(cuadCont, operador, operando1.varDir, operando2.varDir, operandoTemp.varDir)
        cuadruplos.append(cuadruplo)
        cuadCont += 1

        pilaOperandos.append(operandoTemp)
        t[0]=t[1]


      else:
        print("Error Semantico: valores incompatibles en suma")
        sys.exit()
    pass

def p_push_opt(t):
    'push_opt : empty'
    global pilaOperadores
    pilaOperadores.append(t[-1])


def p_exp_uminus(t):
    'exp : MENOS exp %prec UMINUS'
    t[0] = -t[2]
 

def p_exp_int(t):
    'exp : CTEENTERO'
    global memoria
    memoria = asigna_memoria_constante('entero')
    consInsert(t[1],'entero',memoria)
    consVar = varTableNode('cte', None, 'entero', consGetDir(t[1]))
    pilaOperandos.append(consVar)
    t[0] = t[1]

def p_exp_float(t):
    'exp : CTEFLOTANTE'
    global memoria
    memoria = asigna_memoria_constante('flotante')
    consInsert(t[1],'flotante',memoria)
    consVar = varTableNode('cte', None, 'flotante', consGetDir(t[1]))
    pilaOperandos.append(consVar)
    t[0] = t[1]
pass

def p_exp_booleano(t):
    '''exp : TRUE
          | FALSE'''
    t[0] = t[1]
    global memoria
    memoria = asigna_memoria_constante('booleano')
    consInsert(t[1],'booleano',memoria)
    consVar = varTableNode('cte', None, 'booleano', consGetDir(t[1]))
    pilaOperandos.append(consVar)
pass

def p_exp_texto(t):
    'exp : CTETEXTO'
    t[0] = t[1]
    global memoria
    memoria = asigna_memoria_constante('texto')
    consInsert(t[1],'texto',memoria)
    consVar = varTableNode('cte', None, 'texto', consGetDir(t[1]))
    pilaOperandos.append(consVar)

pass

def p_exp_var(t):
    'exp : ID varfuncarr'
    t[0] = t[1]

pass

def p_exp_varfunc(t):
    '''varfuncarr : push_var_opd
                | llamada
                | arraycall'''

pass


def p_push_var_opd(t):
    'push_var_opd : empty'
    if varFind(varGlb,t[-1]):
      auxVar = getVar(varGlb,t-[1])
    else:
      proc = getProc(actualProc)
      auxParams = proc.procParams
      if varFind(auxParams, t[-1]):
        auxVar = getVar(auxParams,t[-1])
      else:
        auxTable = getVarTable(actualProc)
        if varFind(auxTable,t[-1]):
          auxVar = getVar(auxTable,t[-1])
        else:
          print ("Error Semantico: Variable ", t[-1], " no encontrada" )
          sys.exit()
    pilaOperandos.append(auxVar)
pass

def p_llamada(t):
    'llamada : PARENTIZQ llamada_param PARENTDER'
    global cuadCont
    global cuadruplos
    global pilaParams
    if procFind(t[-1]):
      proc = getProc(t[-1])
      #solicitud de memoria
      cuadruplo = Cuadruplo(cuadCont, 'ERA', None , proc.procName, None)
      cuadruplos.append(cuadruplo)
      cuadCont += 1

      #paso de control de ejecucion
      cuadruplo = Cuadruplo(cuadCont, 'GOSUB', None , proc.procName, None)
      cuadruplos.append(cuadruplo)
      cuadCont += 1

      retVar = proc.procRetVar
      print(retVar)
      if retVar != None:
        pilaOperandos.append(retVar)

      paramsFunc = proc.procParams.copy()
      cantParams = 0
      cantParamsFunc = 0

      
      #cantiad de parametros en la llamada
      for param in pilaParams:
        cantParams = cantParams + 1

      #cantidad de parametros en la funcion
      for param in paramsFunc:
        cantParamsFunc = cantParamsFunc + 1

      #se evalua la cantidad de parametros
      if cantParams == cantParamsFunc:
        #se coloca en orden de comparacion en caso de ser multiples parametros
        if cantParams>=1:
          aux = pilaParams.pop()
          pilaParams.insert(0,aux)
          paramsFunc.reverse()
          while cantParams:
            #se comparan parametros de llmada y de funcion
            paramFunc = paramsFunc.pop()
            paramLlam = pilaParams.pop()
            if paramFunc.varType != paramLlam.varType:
              print('Parametros incompatibles en llamada a funcion ', t[-1])
              sys.exit()
            cuadruplo = Cuadruplo(cuadCont, 'PARAM', paramLlam.varDir , None, None)
            cuadruplos.append(cuadruplo)
            cuadCont += 1
            cantParams = cantParams - 1

      else:
        print('Cantidad de parametros en llamada de la funcion ', t[-1],'es incorrecta')
        sys.exit()
    else:
      print('El procedimiento ', t[-1],' no ha sido declarado')
      sys.exit()

pass

def p_llamada_param(t): 
    'llamada_param : expresion llamada_param_mult'
    global pilaParams
    global pilaOperandos
    param = pilaOperandos.pop()
    pilaParams.append(param)
pass

def p_expresion_unique(t): 
    'expresion : exp'
    t[0] = t[1]
pass
 

def p_llamada_param_mult(t):
    'llamada_param_mult :  llamada_param_mult COMA expresion'
    global pilaParams
    global pilaOperandos
    param = pilaOperandos.pop()
    pilaParams.append(param)
pass

def p_llamada_param_mult_empty(t):
    'llamada_param_mult : empty'
pass

def p_llamada_param_empty(t):
    'llamada_param : empty'
pass

def p_arraycall(t): 
    'arraycall : CORCHETEIZQ exp CORCHETEDER'
    global cuadruplos
    global cuadCont
    global pilaOperandos
    global tempCont

    if varFind(varGlb,t[-1]):
      auxVar = getVar(varGlb,t[-1])
    else:
      auxTable = getVarTable(actualProc)
      if varFind(auxTable,t[-1]):
        auxVar = getVar(auxTable,t[-1])
      else:
        print ("Error Semantico: Variable de tipo vector ", t[-1], " no encontrada" )
        sys.exit()
  
    index = pilaOperandos.pop()

    cuadruplo = Cuadruplo(cuadCont, 'VER',index.varDir,0, auxVar.varDim-1)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    memoria = asigna_memoria_temporal('entero')
    operandoTemp = varTableNode('t'+str(tempCont), None, 'entero', memoria)
    tempInsert(operandoTemp)
    tempCont += 1


    cuadruplo = Cuadruplo(cuadCont, 'ARYCA', index.varDir, auxVar.varDir, operandoTemp.varDir)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

  
    pilaOperandos.append(operandoTemp)
    t[0]=t[1]

pass

 
def p_condicion(t):
    'condicion : SI expresion actSi1 ENTONCES bloque actSi2 condicion_else actSi3 FINSI'
    pass

def p_actSi1(t):
    'actSi1   : empty'
    global pilaSaltos
    global cuadruplos
    global cuadCont
    global pilaOperandos

    pilaSaltos.append(cuadCont)
    tempOperando = pilaOperandos.pop()
    cuadruplo = Cuadruplo(cuadCont, 'GOTOF',tempOperando.varDir , None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    pass

def p_bloque(t):
    'bloque   : INICIOBLOQUE bloque_estatuto_mult FINBLOQUE'
    pass

def p_bloque_estatuto_mult(t):
    '''bloque_estatuto_mult        : bloque_estatuto_mult estatuto 
               | empty'''
    pass

def p_actSi2(t):
    'actSi2   : empty'
    global pilaSaltos
    global cuadruplos
    global cuadCont

    cuadruplo = Cuadruplo(cuadCont, 'GOTO',None , None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    salto = pilaSaltos.pop()
    for cuad in cuadruplos:
      if cuad.num == salto:
        cuad.opd2= cuadCont
    pilaSaltos.append(cuadCont-1)
    pass

def p_condicion_else(t):
    '''condicion_else : SINO bloque
               | empty'''
    pass

def p_actSi3(t):
    'actSi3   : empty'
    global pilaSaltos
    global cuadruplos
    global cuadCont

    salto = pilaSaltos.pop()
    for cuad in cuadruplos:
      if cuad.num == salto:
        cuad.opd2= cuadCont
    pass

def p_ciclo(t):
    'ciclo    : MIENTRAS actCic1 expresion actCic2 HACER bloque FINMIENTRAS actCic3'
    pass

def p_actCic1(t):
    'actCic1    : empty'
    global pilaSaltos
    global cuadruplos
    global cuadCont

    pilaSaltos.append(cuadCont)

    pass

def p_actCic2(t):
    'actCic2    : empty'
    global pilaSaltos
    global cuadruplos
    global cuadCont

    tempOperando = pilaOperandos.pop()
    cuadruplo = Cuadruplo(cuadCont, 'GOTOF',tempOperando.varDir , None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1
    pilaSaltos.append(cuadCont-1)
    
    pass

def p_actCic3(t):
    'actCic3    : empty'
    global pilaSaltos
    global cuadruplos
    global cuadCont

    salto = pilaSaltos.pop()
    for cuad in cuadruplos:
      if cuad.num == salto:
        cuad.opd2= cuadCont+1

    salto = pilaSaltos.pop()
    cuadruplo = Cuadruplo(cuadCont, 'GOTO', None, salto, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    pass
 
def p_io_cout(t):
    'io : DECIRALUSUARIO exp PUNTOCOMA'
    global cuadruplos
    global cuadCont
    global pilaOperandos
    operando1 = pilaOperandos.pop()
    cuadruplo = Cuadruplo(cuadCont, 'PRINT', operando1.varDir , None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1
    pass
def p_io_cin(t):
    'io : PEDIRALUSUARIO PARENTIZQ ID asignacion_arreglo PARENTDER PUNTOCOMA'
    global cuadruplos
    global cuadCont
    global pilaOperandos
    global tempCont
    global memoria
    
    if varFind(varGlb,t[3]):
      auxVar = getVar(varGlb,t[3])
    else:
      auxTable = getVarTable(actualProc)
      if varFind(auxTable,t[3]):
        auxVar = getVar(auxTable,t[3])
      else:
        print ("Error Semantico: Variable de tipo vector ", t[3], " no encontrada" )
        sys.exit()

    memoria = asigna_memoria_temporal(auxVar.varType)
    operandoTemp = varTableNode('t'+str(tempCont), None, auxVar.varType, memoria)
    tempInsert(operandoTemp)
    tempCont += 1

    cuadruplo = Cuadruplo(cuadCont, 'INPUT', auxVar.varType , None, operandoTemp.varDir)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    if t[4] == None:
      resType = cubo_semantico[auxVar.varType][operandoTemp.varType]['=']
      if resType != "error":
        cuadruplo = Cuadruplo(cuadCont, '=',operandoTemp.varDir , None, auxVar.varDir)
        cuadruplos.append(cuadruplo)
        cuadCont += 1
      else:
        print ("Error Semantico: Variable ", auxVar.varType, " incompatible con valor ",t[4], " a asignar")
        sys.exit()
    else:
      index = pilaOperandos.pop()
      resType = cubo_semantico[auxVar.varType][operandoTemp.varType]['=']
      if resType != "error" and index.varType == "entero":
        # Verifica el indice del arreglo
        cuadruplo = Cuadruplo(cuadCont, 'VER', index.varDir, 0, auxVar.varDim-1)
        cuadruplos.append(cuadruplo)
        cuadCont += 1
        # Genera el temporal
        memoria = asigna_memoria_temporal(resType)
        operandoTemp2 = varTableNode('t'+str(tempCont), None, resType, memoria)
        tempInsert(operandoTemp2)
        tempCont += 1
        # Asigna al temporal la direccion del arreglo + el offset
        cuadruplo = Cuadruplo(cuadCont, 'OFST', index.varDir, auxVar.varDir, operandoTemp2.varDir)
        cuadruplos.append(cuadruplo)
        cuadCont += 1
        # Asigna el valor al arreglo
        cuadruplo = Cuadruplo(cuadCont, 'ARYAS', operandoTemp.varDir, index.varDir, operandoTemp2.varDir)
        cuadruplos.append(cuadruplo)
        cuadCont += 1
      else:
        print ("Error Semantico: Variable ", auxVar.varType, " incompatible con valor ",t[5], " a asignar")
        sys.exit()
      pilaOperandos.append(auxVar)


    pass

def p_accion(t):
    'accion   : tipo_accion PUNTOCOMA'

    pass
 
def p_tipo_accion(t):
    '''tipo_accion : objeto_con_exp
               | objeto_sin_exp'''
    pass

def p_objeto_con_exp(t):
    '''objeto_con_exp  : GIRARDERECHA exp
               | GIRARIZQUIERDA exp
               | MOVER exp '''
    global cuadruplos
    global cuadCont
    global pilaOperandos
    operando1 = pilaOperandos.pop()
    cuadruplo = Cuadruplo(cuadCont, t[1], operando1.varDir , None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1
    pass

def p_objeto_sin_exp(t):
    '''objeto_sin_exp   : BORRAR
               | PINTAR
               | DESPINTAR '''
    global cuadruplos
    global cuadCont
    cuadruplo = Cuadruplo(cuadCont, t[1], None, None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1
    pass

def p_llamada_sin_ret(t):
    'llamada_sin_ret   : ID llamada PUNTOCOMA'
    pass

def p_return(t): 
    'return : REGRESA expresion PUNTOCOMA'
    global cuadCont
    global cuadruplos
    global procTable
    # cuadruplo = Cuadruplo(cuadCont, 'ENDPROC',None , None, None)
    # cuadruplos.append(cuadruplo)
    # cuadCont += 1
    # returnVar = pilaOperandos.pop()
    # proc = getProc(actualProc)
    # proc.procRetVar = returnVar
    # if returnVar.varType != proc.procReturn:
    #   print ("Error Semantico: Valor de retorno incompatible con tipo de funcion ",proc.procReturn, " en ", actualProc )
    #   sys.exit()
    pass

def p_principal(t): 
    'principal : iniciomain vars C FINPRINCIPAL'
    global cuadruplos
    global cuadCont
    cuadruplo = Cuadruplo(cuadCont,'ENDPROG', None, None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1
    pass

def p_iniciomain(t): 
    'iniciomain : INICIOPRINCIPAL'
    global actualProc
    actualProc = 'main'
    procInsert(actualProc, actualProc, cuadCont)
    pass


def p_error(p):
    if p:
        print("Error de sintaxis en: '%s'" % p.value + p.type + ", Linea: %s"%p.lineno)
        sys.exit()
    else:
        print("Error de sintaxis")
        sys.exit()


import ply.yacc as yacc
yacc.yacc(method = 'LALR')

program = []
for line in fileinput.input():
    program.append(line)
yacc.parse(' '.join(program))

