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
             'finprograma'    : 'FINPROGRAMA', 
             'iniciofuncion' : 'INICIOFUNCION', 
             'finfuncion'     : 'FINFUNCION', 
             'parametros'   : 'PARAMETROS', 
             'crear'     : 'CREAR', 
             'dibujar'   : 'DIBUJAR',
             'borrar'    : 'BORRAR',
             'girar'    : 'GIRAR',
             'mover'    : 'MOVER',
             'derecha'    : 'DERECHA',
             'izquierda'    : 'IZQUIERDA',
             'arriba'    : 'ARRIBA',
             'abajo'    : 'ABAJO',
             'si': 'SI',
             'finsi': 'FINSI',
             'entonces': 'ENTONCES',
             'sino': 'SINO',
             'mintras': 'MIENTRAS',
             'finmientras': 'FINMIENTRAS',
             'hacer': 'HACER',
             'pintar': 'PINTAR',
             'nopintar': 'NOPINTAR',
             'lista': 'LISTA',
             'agregar': 'AGREGAR',
             'sacar': 'SACAR',
             'deciralusuario': 'DECIRALUSUARIO',
             'pediralusuario': 'PEDIRALUSUARIO',
             'iniciobloque': 'INICIOBLOQUE',
             'finbloque': 'FINBLOQUE',
             'entero': 'ENTERO',
             'flotante': 'FLOTANTE',
             'texto': 'TEXTO',
             'inicioprincipal': 'INICIOPRINCIPAL',
             'finprincipal': 'FINPRINCIPAL',
             'x': 'X',
             'y': 'Y'
              }

t_CTEENTERO              = r'[0-9]+'
t_CTEFLOTANTE            = r'[0-9]+\.[0-9]+ '
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
T_FALSE             = r'[0]'

t_ignore            = " \t"

def t_ID(t):
    r'[A-Za-z]+[A-Za-z0-9]*'
    t.type = reserved.get(t.value,"ID")
    return t

def t_newline(t):
    r'\n+'
    
def t_error(t):
    print("Caracter no valido'%s'" % t.value[0])
    t.lexer.skip(1)

def p_program(t): 
    'program : INICIOPROGRAMA A cuerpo FINPROGRAMA'
    pass

def p_A(t): 
    '''A : vars
           | empty'''
    pass

def p_vars(t): 
    '''vars : CREAR tipo ID PUNTOCOMA vars
           | empty'''
    pass

 
def p_cuerpo(t): 
    'cuerpo : B principal'
    pass
 
def p_B(t): 
    '''B : funcion B
           | empty'''
    pass
 
def p_funcion(t): 
    'funcion : INICIOFUNCION variable ID parametros C REGRESA expresion FINFUNCION'
    pass

 
def p_variable(t): 
    '''variable : ENTERO
            | FLOTANTE
            | TEXTO'''
    pass
 
def p_C(t): 
    '''C : estatuto
           | empty'''
    pass
 
def p_parametros(t): 
    '''parametros : PARAMETROS tipo ID E
           | empty'''

 
def p_E(t): 
    '''E : COMA tipo ID E
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
    pass
 
def p_H(t): 
    '''H : MULT factor
           | DIV factor
           | empty'''
    pass
 
def p_factor(t): 
    '''factor : PARENTIZQ expresion PARENTDER
           | I varcte'''
    pass


def p_I(t):
    '''I : MAS
           | MENOS
           | empty '''
pass
 
def p_varcte(t):
    '''varcte : ID
           | CTETEXTO
           | CTEFLOTANTE
           | CTEENTERO
           | llamada '''
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
    pass

def p_principal(t): 
    'principal : INICIOPRINCIPAL C FINPRINCIPAL'
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



