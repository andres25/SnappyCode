# snappycodeParser.py

from ply.lex import TOKEN
import sys
import snappycodeLex
import fileinput
from procVarTables import *

tokens = snappycodeLex.tokens

varGlb = {} 
#varFunc = {}
#scope = "global"
actualProc = "global"
#params = {}

precedence = (
    ('nonassoc', 'MAYORQUE', 'MENORQUE', 'DIFERENTEQUE', 'IGUALQUE', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','MULT','DIV'),
    ('right','UMINUS'),
    )

def p_program(t): 
    'program : INICIOPROGRAMA A cuerpo FINPROGRAMA'
    #print("\nCUMPLE CON TODAS LAS REGLAS.\n")
    #print("\nVariables Globales.\n")
    #print (varGlb)
    #print("\nProcedure table.\n")
    #print (procTable)
    pass

def p_A(t): 
    '''A : vars
           | empty'''
    pass

def p_vars(t): 
    '''vars : CREAR tipo ID PUNTOCOMA vars
           | empty'''
    if t[1] != None:
      global scope
      if t[2] == 'entero':
        vDir = 0
      elif t[2] == 'flotante':
        vDir = 0.0
      elif t[2] == 'texto':
        vDir = ' '
      elif t[2] == 'booleano':
        vDir = True

      if actualProc == 'global':
        #varGlb[t[3]] = {'type' : t[2], 'scope' : scope, 'val': aux}
        varGlbInsert(t[3], t[2], vDir)
      else:
        #varFunc[t[3]] = {'type' : t[2], 'scope' : scope,'val': aux}
        varLocInsert(t[3], t[2], vDir, actualProc)
    pass

 
def p_cuerpo(t): 
    'cuerpo : B principal'
    global procTable
    procPrint(procTable)
    pass
 
def p_B(t): 
    '''B : funcion B
           | empty'''
    pass
 
def p_funcion(t):
    'funcion : iniciofunc paramsfunc varsfunc finfunc'
    pass

def p_iniciofunc(t): 
    'iniciofunc : INICIOFUNCION variable ID'
    t[0]= t[3]
    global scope
    scope = 'parametro'
    global actualProc
    actualProc = t[3]
    pDir = 0
    procInsert(actualProc, t[2], pDir)
    pass

def p_paramsfunc(t): 
    'paramsfunc : param'
    global scope
    scope = 'local'
    pass

def p_varsfunc(t): 
    'varsfunc : vars'
    #aux = params.copy()
    #aux2 = varFunc.copy() 
    #procTable[actualProc] = {'param' : aux , 'return' : t[1], 'symTable': aux2}
    
    #params.clear()
    #varFunc.clear()
    pass

def p_finfunc(t): 
    'finfunc : C REGRESA expresion FINFUNCION'
    pass

 
def p_variable(t): 
    '''variable : ENTERO
            | FLOTANTE
            | TEXTO
            | BOOLEANO'''
    t[0] = t[1]
    pass
 
def p_C(t): 
    '''C : estatuto C
           | empty'''
    pass
 
def p_param(t): 
    '''param : PARAMETROS tipo ID E
           | empty'''
    if t[1] != None:
      #params[t[3]] = {'type' : t[2]}
      if t[2] == 'entero':
        vDir = 0
      elif t[2] == 'flotante':
        vDir = 0.0
      elif t[2] == 'texto':
        vDir = ' '
      elif t[2] == 'booleano':
        vDir = True
      else:
        print("Error de sintaxis en parametros de funcion " + actualProc)
      paramInsert(t[3], t[2], vDir, actualProc)
    pass     
 
def p_E(t): 
    '''E : COMA tipo ID E
           | empty'''
    if t[1] != None:
      #params[t[3]] = {'type' : t[2]}
      if t[2] == 'entero':
        vDir = 0
      elif t[2] == 'flotante':
        vDir = 0.0
      elif t[2] == 'texto':
        vDir = ' '
      elif t[2] == 'booleano':
        vDir = True
      else:
        print("Error de sintaxis en parametros de funcion " + actualProc)
      paramInsert(t[3], t[2], vDir, actualProc)
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
    pass
 
def p_expresion_eval(t): 
    '''expresion : exp MAYORQUE exp
           | exp MENORQUE exp
           | exp DIFERENTEQUE exp
           | exp IGUALQUE exp
           | exp MAYORIGUAL exp
           | exp MENORIGUAL exp'''
    if t[2] == '>'  : t[0] = t[1] > t[3]
    elif t[2] == '<': t[0] = t[1] < t[3]
    elif t[2] == '!=': t[0] = t[1] != t[3]
    elif t[2] == '==': t[0] = t[1] == t[3]
    elif t[2] == '>=': t[0] = t[1] >= t[3]
    elif t[2] == '<=': t[0] = t[1] <= t[3]

    pass

def p_expresion_empty(t): 
    '''expresion : exp '''
    t[0] = t[1]
    pass


 
def p_exp_binop(t):
    '''exp : exp MAS exp
                  | exp MENOS exp
                  | exp MULT exp
                  | exp DIV exp'''

def p_exp_uminus(t):
    'exp : MENOS exp %prec UMINUS'
    t[0] = -t[2]
 
def p_exp_agrupacion(t): 
    'exp : PARENTIZQ expresion PARENTDER'
    t[0] = t[2]
    pass

def p_exp_num(t):
    '''exp : CTEENTERO
          | CTEFLOTANTE '''
    t[0] = t[1]
    pass

def p_exp_booleano(t):
    '''exp : TRUE
          | FALSE '''
    if t[1] == 'TRUE': t[0] = 1
    else:
      t[0] = 0 
    pass

def p_exp_var(t):
    'exp : ID'
    try:
        #print (procTable[scope])
        t[0] = 1
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0
 
def p_exp_texto(t):
    '''varcte : CTETEXTO
           | llamada '''
    t[0] = t[1]
pass
 
def p_llamada(t):
    'llamada : ID L'
pass
 
def p_L(t):
    '''L : PARAMETROS expresion M
           | empty  '''
pass
 
def p_M(t):
    '''M : COMA expresion M
           | empty  '''
pass
 
def p_condicion(t):
    'condicion : SI expresion ENTONCES bloque J FINSI'
    pass
 
def p_J(t):
    '''J : SINO bloque
               | empty '''
    pass
 
def p_ciclo(t):
    'ciclo    : MIENTRAS expresion HACER bloque FINMIENTRAS'
    pass
 
def p_io(t):
    '''io : PEDIRALUSUARIO ID
               | DECIRALUSUARIO expresion '''
    pass
 
def p_accion(t):
    'accion   : tipo_accion O ID PUNTOCOMA'
    pass
 
def p_tipo_accion(t):
    '''tipo_accion : lista
               | objeto '''
    pass
 
def p_objeto(t):
    '''objeto   : CREAR
               | DIBUJAR
               | BORRAR
               | GIRAR
               | PINTAR
               | DESPINTAR
               | MOVER '''
    pass
 
def p_O(t):
    '''O        : X expresion
               | Y expresion
               | DERECHA
               | IZQUIERDA
               | ARRIBA
               | ABAJO
               | empty  '''
    pass
 
def p_lista(t):
    '''lista    : AGREGAR
               | SACAR
               | VER '''
    pass
 
def p_bloque(t):
    'bloque   : INICIOBLOQUE K FINBLOQUE'
    pass
 
def p_K(t):
    '''K        : estatuto K
               | empty '''
    pass
 
def p_tipo(t):
    '''tipo     : variable
               | LISTA '''
    t[0] = t[1]
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

def p_empty(t):
    'empty : '
    pass

def p_error(p):
    if p:
        print("Error de sintaxis en: '%s'" % p.value + p.type)
    else:
        print("Error de sintaxis")

import ply.yacc as yacc
yacc.yacc()

program = []
for line in fileinput.input():
	program.append(line)
yacc.parse(' '.join(program))

