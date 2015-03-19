from ply.lex import TOKEN
import sys
if sys.version_info[0] >= 3:
    raw_input = input


#Definicion de los Tokens
  

tokens = ( 'INICIOPROGRAMA', 'FINPROGRAMA', 'INICIOFUNCION', 'FINFUNCION', 'REGRESA', 'PARAMETROS',
    'CREAR','DIBUJAR','BORRAR','GIRAR','ID','TRUE','FALSE', 'INICIOPRINCIPAL', 'FINPRINCIPAL',
    'MOVER','DERECHA','IZQUIERDA','ARRIBA','ABAJO','SI','FINSI' ,'ENTONCES',
    'SINO','MIENTRAS','FINMIENTRAS','HACER','LISTA','AGREGAR', 'X', 'Y',
    'SACAR', 'VER','IGUAL', 'IGUALQUE' , 'MAYORQUE' , 'MENORQUE', 'DIFERENTEQUE', 'PINTAR', 
    'DESPINTAR', 'DECIRALUSUARIO', 'PEDIRALUSUARIO', 'INICIOBLOQUE', 'FINBLOQUE', 'MAS','MENOS','COMA',
    'MULT', 'DIV', 'PUNTOCOMA','PARENTIZQ','PARENTDER', 'ENTERO', 'FLOTANTE', 'TEXTO', 'CTEENTERO', 'CTEFLOTANTE', 'CTETEXTO'
    )

reserved = { 'inicioprograma' : 'INICIOPROGRAMA', 
              'INICIOPROGRAMA' : 'INICIOPROGRAMA',
             'finprograma'    : 'FINPROGRAMA', 
             'FINPROGRAMA'    : 'FINPROGRAMA',
             'iniciofuncion' : 'INICIOFUNCION',
             'INICIOFUNCION' : 'INICIOFUNCION', 
             'finfuncion'     : 'FINFUNCION', 
             'FINFUNCION'     : 'FINFUNCION', 
             'parametros'   : 'PARAMETROS', 
             'PARAMETROS'   : 'PARAMETROS', 
             'VER'       : 'VER',
             'ver'       : 'ver',
             'REGRESA'   : 'REGRESA',
             'regresa'   : 'regresa',
             'crear'     : 'CREAR', 
             'CREAR'     : 'CREAR', 
             'dibujar'   : 'DIBUJAR',
             'DIBUJAR'   : 'DIBUJAR',
             'borrar'    : 'BORRAR',
             'BORRAR'    : 'BORRAR',
             'girar'    : 'GIRAR',
             'GIRAR'    : 'GIRAR',
             'mover'    : 'MOVER',
             'MOVER'    : 'MOVER',
             'derecha'    : 'DERECHA',
             'DERECHA'    : 'DERECHA',
             'izquierda'    : 'IZQUIERDA',
             'IZQUIERDA'    : 'IZQUIERDA',
             'arriba'    : 'ARRIBA',
             'ARRIBA'    : 'ARRIBA',
             'abajo'    : 'ABAJO',
             'ABAJO'    : 'ABAJO',
             'si': 'SI',
             'SI': 'SI',
             'finsi': 'FINSI',
             'FINSI': 'FINSI',
             'entonces': 'ENTONCES',
             'ENTONCES': 'ENTONCES',
             'sino': 'SINO',
             'SINO': 'SINO',
             'mintras': 'MIENTRAS',
             'MIENTRAS': 'MIENTRAS',
             'finmientras': 'FINMIENTRAS',
             'FINMIENTRAS': 'FINMIENTRAS',
             'hacer': 'HACER',
             'HACER': 'HACER',
             'pintar': 'PINTAR',
             'PINTAR': 'PINTAR',
             'nopintar': 'NOPINTAR',
             'NOPINTAR': 'NOPINTAR',
             'lista': 'LISTA',
             'LISTA': 'LISTA',
             'agregar': 'AGREGAR',
             'AGREGAR': 'AGREGAR',
             'sacar': 'SACAR',
             'SACAR': 'SACAR',
             'deciralusuario': 'DECIRALUSUARIO',
             'DECIRALUSUARIO': 'DECIRALUSUARIO',
             'pediralusuario': 'PEDIRALUSUARIO',
             'PEDIRALUSUARIO': 'PEDIRALUSUARIO',
             'iniciobloque': 'INICIOBLOQUE',
             'INICIOBLOQUE': 'INICIOBLOQUE',
             'finbloque': 'FINBLOQUE',
             'FINBLOQUE': 'FINBLOQUE',
             'entero': 'ENTERO',
             'ENTERO': 'ENTERO',
             'flotante': 'FLOTANTE',
             'FLOTANTE': 'FLOTANTE',
             'texto': 'TEXTO',
             'TEXTO': 'TEXTO',
             'inicioprincipal': 'INICIOPRINCIPAL',
             'INICIOPRINCIPAL': 'INICIOPRINCIPAL',
             'finprincipal': 'FINPRINCIPAL',
             'FINPRINCIPAL': 'FINPRINCIPAL',
             'x': 'X',
             'X': 'X',
             'y': 'Y',
             'Y': 'Y',
              }

t_CTETEXTO               = r'"\"".+"\""'
t_PUNTOCOMA              = r';'
t_PARENTIZQ              = r'\('
t_PARENTDER              = r'\)'
t_IGUAL                  = r'='
t_IGUALQUE            = r'=='
t_MAS              = r'\+'
t_MENOS             = r'-'
t_DIV          = r'\/'
t_MULT              = r'\*'
t_MENORQUE              = r'<'
t_MAYORQUE           = r'>'
t_DIFERENTEQUE         = r'<>'
t_COMA             = r','
t_TRUE              = r'[1]'
t_FALSE             = r'[0]'

t_ignore            = " \t"

varGlb = {} 
varFunc = {}
scope = "Indefinido"
params = {}
procTable = {}

def t_ID(t):
    r'[A-Za-z]+[A-Za-z0-9]*'
    t.type = reserved.get(t.value,"ID")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_CTEENTERO(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CTEFLOTANTE(t):
    r'[0-9]+\.[0-9]+ '
    t.value = float(t.value)
    return t    
    
def t_error(t):
    print("Caracter no valido'%s'" % t.value[0])
    t.lexer.skip(1)

def p_program(t): 
    'program : INICIOPROGRAMA A cuerpo FINPROGRAMA'
    print("\nCUMPLE CON TODAS LAS REGLAS.\n")
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
      if scope == 'global':
        varGlb[t[3]] = {'type' : t[2], 'scope' : scope}
      else:
        varFunc[t[3]] = {'type' : t[2], 'scope' : scope}
    else:
      if scope == 'Indefinido':
        scope = 'global'
      else:
        scope = 'funcion'
    pass

 
def p_cuerpo(t): 
    'cuerpo : B principal'
    pass
 
def p_B(t): 
    '''B : funcion B
           | empty'''
    pass
 
def p_funcion(t):
    'funcion : INICIOFUNCION variable ID param vars C REGRESA expresion FINFUNCION'
    if t[1] != None:
      for key, value in varFunc.items():
        if value['scope'] == 'funcion':
          varFunc[key]['scope'] = t[3]

      aux = params.copy()
      aux2 = varFunc.copy() 
      procTable[t[3]] = {'param' : aux , 'return' : t[2], 'symTable': aux2}
      params.clear()
      varFunc.clear()
    pass

 
def p_variable(t): 
    '''variable : ENTERO
            | FLOTANTE
            | TEXTO'''
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
      params[t[3]] = {'type' : t[2]}
       
    pass     
 
def p_E(t): 
    '''E : COMA tipo ID E
           | empty'''
    if t[1] != None:
      params[t[3]] = {'type' : t[2]}
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
 
def p_expresion(t): 
    'expresion : exp F'
    pass
 
def p_F(t): 
    '''F : MAYORQUE exp
           | MENORQUE exp
           | DIFERENTEQUE exp
           | IGUALQUE exp
           | empty'''
    pass
 
def p_exp(t): 
    'exp : termino G'
    pass
 
def p_G(t): 
    '''G : MAS termino
           | MENOS termino
           | empty'''
    pass
 
def p_termino(t): 
    'termino : factor H'
    #print(t[2])
    pass
 
def p_H(t): 
    '''H : MULT factor
           | DIV factor
           | empty'''
    if t[1] == '*':
      t[0]= '*'
    elif t[1] == '/':
      t[0]= '/'
    print(t[0])
    pass
 
def p_factor(t): 
    '''factor : PARENTIZQ expresion PARENTDER
           | I varcte'''
    if t[1] == '-':
      t[0] = (-1)*t[1]
    pass
    pass


def p_I(t):
    '''I : MAS
           | MENOS
           | empty '''
    if t[1] == '-':
      t[0] = t[1]
    else:
      t[0] = '+'
    pass
 
def p_varcte(t):
    '''varcte : ID
           | CTETEXTO
           | CTEFLOTANTE
           | CTEENTERO
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
    'principal : INICIOPRINCIPAL C FINPRINCIPAL'
    global scope
    scope = 'main'
    pass

def p_empty(t):
    'empty : '
    pass

def p_error(p):
    if p:
        print("Error de sintaxis en: '%s'" % p.value + p.type)
    else:
        print("Error de sintaxis")


entrada = open ("test.in", "r");

import ply.lex as lex
lex.lex()
import ply.yacc as yacc
yacc.yacc()
yacc.parse(entrada.read())



