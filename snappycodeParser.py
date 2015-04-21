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
    'vars : vars CREAR tipo ID PUNTOCOMA '
    global memoria
    if actualProc == 'global':
      asigna_memoria_global(t[3])
      varGlbInsert(t[4], None, t[3], memoria)
    else:
      asigna_memoria_local(t[3])
      varLocInsert(t[4], None, t[3], memoria, actualProc)
    pass

def p_tipo(t):
    '''tipo   : ENTERO
              | FLOTANTE
              | TEXTO
              | BOOLEANO
              | LISTA'''
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
    pDir = 0
    procInsert(actualProc, t[2], pDir)
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
      cuadruplo = Cuadruplo(cuadCont, '=',tempOperando.varDir , None, resDir.varDir)
      cuadruplos.append(cuadruplo)
      cuadCont += 1
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
        print("Error Semantico: valores incompatibles en la comparación") 
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

def p_exp_var(t):
    'exp : ID push_var_opd'
    t[0] = t[1]

pass

def p_push_var_opd(t):
    'push_var_opd : '
    if varFind(varGlb,t[-1]):
      auxVar = getVar(varGlb,t-[1])
      auxVal = auxVar.varVal
      pilaOperandos.append(auxVal)
    else:
      auxTable = getVarTable(actualProc)
      if varFind(auxTable,t[-1]):
        auxVar = getVar(auxTable,t[-1])
        auxVal = auxVar.varVal
        pilaOperandos.append(auxVal)
      else:
        print ("Error Semantico: Variable ", t[-1], " no encontrada" )
pass

def p_exp_texto(t):
    '''exp : CTETEXTO'''
    t[0] = t[1]
    global memoria
    asigna_memoria_constante('texto')
    consInsert(t[1],'texto',memoria)
    consVar = varTableNode('cte', None, 'texto', consGetDir(t[1]))
    pilaOperandos.append(consVar)

pass


#def p_exp_llamada(t):
#    'exp :  llamada'
#    t[0] = t[1]
#pass

#def p_llamada(t):
#    'llamada : ID llamada_param'
#pass

#def p_llamada_param(t):
#    '''llamada_param : PARAMETROS expresion llamada_param_mult
#           | empty'''
#pass
def p_expresion_unique(t): 
    'expresion : exp'
    t[0] = t[1]
    pass
 

#def p_llamada_param_mult(t):
#    '''llamada_param_mult :  llamada_param_mult COMA expresion 
#           | empty'''
#pass
 
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
    cuadruplo = Cuadruplo(cuadCont, 'GOTO',None , salto, None)
    cuadruplos.append(cuadruplo)
    cuadCont += 1

    pass
 
def p_io(t):
    '''io : PEDIRALUSUARIO ID
               | DECIRALUSUARIO expresion'''
    pass
 
def p_accion(t):
    'accion   : tipo_accion ID PUNTOCOMA'
    pass
 
def p_tipo_accion(t):
    '''tipo_accion : lista
               | objeto'''
    pass

def p_lista(t):
    '''lista : lista_agregar
               | lista_sacar
               | lista_ver'''
    pass

def p_lista_agregar(t):
    'lista_agregar : AGREGAR'

    pass

def p_lista_sacar(t):
    'lista_sacar : SACAR'

    pass

def p_lista_ver(t):
    'lista_ver : VER'

    pass
 
def p_objeto(t):
    '''objeto   : 
               | objeto_con_expresion 
               | objeto_sin_expresion'''
    pass

def p_objeto_con_expresion(t):
    '''objeto_con_expresion  : GIRAR DERECHA expresion
               | MOVER expresion '''
    pass

def p_objeto_sin_expresion(t):
    '''objeto_sin_expresion   : BORRAR 
               | GIRAR IZQUIERDA
               | PINTAR
               | DESPINTAR '''
    pass

def p_principal(t): 
    'principal : iniciomain vars C FINPRINCIPAL'

    pass

def p_iniciomain(t): 
    'iniciomain : INICIOPRINCIPAL'
    global actualProc
    actualProc = 'main'
    pDir = 0
    procInsert(actualProc, actualProc, pDir)
    pass


def p_error(p):
    if p:
        print("Error de sintaxis en: '%s'" % p.value + p.type)
    else:
        print("Error de sintaxis")

def asigna_memoria_global(tipo):
    global EnteroGlobal
    global FlotanteGlobal
    global TextoGlobal
    global BooleanGlobal
    global memoria 
    if tipo == 'entero' or tipo == 'ENTERO':
      memoria = EnteroGlobal
      EnteroGlobal += 1
    elif tipo == 'flotante' or tipo == 'FLOTANTE':
      memoria = FlotanteGlobal
      FlotanteGlobal += 1
    elif tipo == 'texto' or tipo == 'TEXTO':
      memoria = TextoGlobal
      TextoGlobal += 1
    elif tipo == 'booleano' or tipo == 'BOOLEANO':
      memoria = BooleanGlobal
      BooleanGlobal += 1

def asigna_memoria_local(tipo):
    global EnteroLocal
    global FlotanteLocal
    global TextoLocal
    global BooleanLocal
    global memoria 
    if tipo == 'entero' or tipo == 'ENTERO':
      memoria = EnteroLocal
      EnteroLocal += 1
    elif tipo == 'flotante' or tipo == 'FLOTANTE':
      memoria = FlotanteLocal
      FlotanteLocal += 1
    elif tipo == 'texto' or tipo == 'TEXTO':
      memoria = TextoLocal
      TextoLocal += 1
    elif tipo == 'booleano' or tipo == 'BOOLEANO':
      memoria = BooleanLocal
      BooleanLocal += 1

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

