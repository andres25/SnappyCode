# snappycodeParser.py

from ply.lex import TOKEN
import sys
import snappycodeLex
import fileinput
from cuadruplo import *
from procVarTables import *
from memoria import *
from cubosemantico import *

tokens = snappycodeLex.tokens
actualProc = "global"
memoria = 0
pilaOperadores = []
pilaOperandos = []
tempCont = 0
cuadruplos = []
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
    procPrint(procTable)
    global cuadruplos
    print ("Cuadruplos")
    for cuad in cuadruplos:
        print(cuad.num, '|', cuad.opt, '|', cuad.opd1, '|', cuad.opd2, '|', cuad.res , '\n')
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
      asigna_memoria_global(t[2])
      varGlbInsert(t[3], None, t[2], memoria)
    else:
      asigna_memoria_local(t[2])
      varLocInsert(t[3], None, t[2], memoria, actualProc)
    pass

def p_array(t):
    'array : CREAR tipo ID CORCHETEIZQ CTEENTERO CORCHETEDER PUNTOCOMA'
    global memoria
    if actualProc == 'global':
      asigna_memoria_global(t[2], t[5])
      varGlbInsert(t[3], None, t[2], memoria, t[5])
    else:
      asigna_memoria_local(t[2], t[5])
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
    procInsert(actualProc, procType, cuadCont)
    pass

def p_param(t): 
    'param : PARAMETROS tipo ID param_mult'
    global scope
    scope = 'local'
    global memoria
      #params[t[3]] = {'type' : t[2]}
    asigna_memoria_local(t[2])
    paramInsert(t[3], t[2], memoria, actualProc)
    pass
     
 
def p_param_mult(t): 
    'param_mult : COMA tipo ID param_mult'
    global memoria
    asigna_memoria_local(t[2])
    paramInsert(t[3], t[2], memoria, actualProc)
    pass

def p_param_mult_empty(t): 
    'param_mult : empty'
    pass

def p_param_empty(t): 
    'param : empty'
    pass 


def p_finfunc(t): 
    'finfunc : C REGRESA expresion FINFUNCION'
    global cuadCont
    global cuadruplos
    global procTable
    cuadruplo = Cuadruplo(cuadCont, 'RETURN',None , None, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1
    returnVar = pilaOperandos.pop()
    proc = getProc(actualProc)
    proc.procRetVar = returnVar
    if returnVar.varType != proc.procReturn:
      print ("Error Semantico: Valor de retorno incompatible con tipo de funcion ",proc.procReturn, " en ", actualProc )
      sys.exit()
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
           | accion'''
    pass
 
def p_asignacion(t): 
    'asignacion : ID IGUAL expresion PUNTOCOMA'
    global varGlb
    global procTable
    global cuadCont
    global tempTable

    if pilaOperandos:
      if varFind(varGlb,t[1]):
        resDir = getVar(varGlb,t[1])
      else:
        auxTable = getVarTable(actualProc)
        if varFind(auxTable,t[1]):
          resDir = getVar(auxTable,t[1])
        else:
          print ("Error Semantico: Variable ", t[1], " no encontrada" )
      tempOperando = pilaOperandos.pop()
      resType = cubo_semantico[resDir.varType][tempOperando.varType]['=']
      if resType != "error":
        cuadruplo = Cuadruplo(cuadCont, '=',tempOperando.varDir , None, resDir.varDir)
        cuadruplos.append(cuadruplo)
        cuadCont += 1
      else:
        print ("Error Semantico: Variable ", t[3], " incompatible con valor ",resDir.varType, " a asignar")
    else:
      print ("Error Semantico: Variable ", t[3], " no se puede asignar" )

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
        asigna_memoria_temporal(resType)
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
        asigna_memoria_temporal(resType)
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
    asigna_memoria_constante('entero')
    consInsert(t[1],'entero',memoria)
    consVar = varTableNode('cte', None, 'entero', consGetDir(t[1]))
    pilaOperandos.append(consVar)
    t[0] = t[1]

def p_exp_float(t):
    'exp : CTEFLOTANTE'
    global memoria
    asigna_memoria_constante('flotante')
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
    asigna_memoria_constante('booleano')
    consInsert(t[1],'booleano',memoria)
    consVar = varTableNode('cte', None, 'booleano', consGetDir(t[1]))
    pilaOperandos.append(consVar)
pass

def p_exp_texto(t):
    'exp : CTETEXTO'
    t[0] = t[1]
    global memoria
    asigna_memoria_constante('texto')
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
      auxTable = getVarTable(actualProc)
      if varFind(auxTable,t[-1]):
        auxVar = getVar(auxTable,t[-1])
      else:
        print ("Error Semantico: Variable ", t[-1], " no encontrada" )
    pilaOperandos.append(auxVar)
pass

def p_llamada(t):
    'llamada : PARENTIZQ llamada_param PARENTDER'
    global cuadCont
    global cuadruplos
    global pilaParams
    if procFind(t[-1]):
      proc = getProc(t[-1])
      cuadruplo = Cuadruplo(cuadCont, 'GOTO',proc.procDir , None, None)
      cuadruplos.append(cuadruplo)
      cuadCont += 1
      retVar = proc.procRetVar
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
        if cantParams>1:
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
            cantParams = cantParams - 1

      else:
        print('Cantidad de parametros en llamada de la funcion ', t[-1],'es incorrecta')
    else:
      print('El procedimiento ', t[-1],' no ha sido declarado')

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
      auxVar = getVar(varGlb,t-[1])
    else:
      auxTable = getVarTable(actualProc)
      if varFind(auxTable,t[-1]):
        auxVar = getVar(auxTable,t[-1])
      else:
        print ("Error Semantico: Variable ", t[-1], " no encontrada" )
  
    index = pilaOperandos.pop()


    asigna_memoria_temporal('entero')
    operandoTemp = varTableNode('t'+str(tempCont), None, 'entero', memoria)
    tempInsert(operandoTemp)
    tempCont += 1


    cuadruplo = Cuadruplo(cuadCont, '+',auxVar.varDir , index.varDir , operandoTemp.varDir)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    
    cuadruplo = Cuadruplo(cuadCont, 'VER',auxVar.varDim , operandoTemp.varDir , None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    pilaOperandos.append(operandoTemp)

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
 
def p_io(t):
    '''io : PEDIRALUSUARIO ID
               | DECIRALUSUARIO exp'''

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

def p_principal(t): 
    'principal : iniciomain vars C FINPRINCIPAL'

    pass

def p_iniciomain(t): 
    'iniciomain : INICIOPRINCIPAL'
    global actualProc
    actualProc = 'main'
    procInsert(actualProc, actualProc, cuadCont)
    pass


def p_error(p):
    if p:
        print("Error de sintaxis en: '%s'" % p.value + p.type)
    else:
        print("Error de sintaxis")

def asigna_memoria_global(tipo, offset = 0):
    global EnteroGlobal
    global FlotanteGlobal
    global TextoGlobal
    global BooleanGlobal
    global memoria 
    if tipo == 'entero' or tipo == 'ENTERO':
      memoria = EnteroGlobal
      EnteroGlobal += 1 + offset
    elif tipo == 'flotante' or tipo == 'FLOTANTE':
      memoria = FlotanteGlobal
      FlotanteGlobal += 1 + offset
    elif tipo == 'texto' or tipo == 'TEXTO':
      memoria = TextoGlobal
      TextoGlobal += 1 + offset
    elif tipo == 'booleano' or tipo == 'BOOLEANO':
      memoria = BooleanGlobal
      BooleanGlobal += 1 + offset

def asigna_memoria_local(tipo, offset = 0):
    global EnteroLocal
    global FlotanteLocal
    global TextoLocal
    global BooleanLocal
    global memoria 
    if tipo == 'entero' or tipo == 'ENTERO':
      memoria = EnteroLocal
      EnteroLocal += 1 + offset
    elif tipo == 'flotante' or tipo == 'FLOTANTE':
      memoria = FlotanteLocal
      FlotanteLocal += 1 + offset
    elif tipo == 'texto' or tipo == 'TEXTO':
      memoria = TextoLocal
      TextoLocal += 1 + offset
    elif tipo == 'booleano' or tipo == 'BOOLEANO':
      memoria = BooleanLocal
      BooleanLocal += 1 + offset

def asigna_memoria_constante(tipo):
    global EnteroConstante
    global FlotanteConstante
    global TextoConstante
    global BooleanConstante
    global memoria 
    if tipo == 'entero' or tipo == 'ENTERO':
      memoria = EnteroConstante
      EnteroConstante += 1
    elif tipo == 'flotante' or tipo == 'FLOTANTE':
      memoria = FlotanteConstante
      FlotanteConstante += 1
    elif tipo == 'texto' or tipo == 'TEXTO':
      memoria = TextoConstante
      TextoConstante += 1
    elif tipo == 'booleano' or tipo == 'BOOLEANO':
      memoria = BooleanConstante
      BooleanConstante += 1

def asigna_memoria_temporal(tipo):
    global EnteroTemporal
    global FlotanteTemporal
    global TextoTemporal
    global BooleanTemporal
    global memoria 
    if tipo == 'entero' or tipo == 'ENTERO':
      memoria = EnteroTemporal
      EnteroTemporal += 1
    elif tipo == 'flotante' or tipo == 'FLOTANTE':
      memoria = FlotanteTemporal
      FlotanteTemporal += 1
    elif tipo == 'texto' or tipo == 'TEXTO':
      memoria = TextoTemporal
      TextoTemporal += 1
    elif tipo == 'booleano' or tipo == 'BOOLEANO':
      memoria = BooleanTemporal
      BooleanTemporal += 1

import ply.yacc as yacc
yacc.yacc(method = 'LALR')

program = []
for line in fileinput.input():
    program.append(line)
yacc.parse(' '.join(program))

