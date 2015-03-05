from ply.lex import TOKEN
import sys
if sys.version_info[0] >= 3:
    raw_input = input


#Definicion de los Tokens
  

tokens = ( 'INICIO_PROGRAMA', 'FIN_PROGRAMA', 'INICIO_FUNCION', 'FIN_FUNCION', 'REGRESA', 'PARAMETROS',
    'CREAR','DIBUJAR','BORRAR','GIRAR','ID','TRUE','FALSE'
    'MOVER','DERECHA','IZQUIERDA','ARRIBA','ABAJO','SI','FIN_SI' ,'ENTONCES',
    'SI_NO','MIENTRAS','FIN_MIENTRAS','HACER','LISTA','AGREGAR',
    'SACAR', 'VER','IGUAL', 'IGUAL_QUE' , 'MAYOR_QUE' , 'MENOR_QUE', 'DIFERENTE_QUE', 'PINTAR', 
    'DESPINTAR', 'DECIR_AL_USUARIO', 'PEDIR_AL_USUARIO', 'INICIO_BLOQUE', 'FIN_BLOQUE', 'MAS','MENOS','COMA',
    'MULT', 'DIV', 'PUNTOCOMA','PARENTIZQ','PARENTDER', 'ENTERO', 'FLOTANTE', 'TEXTO', 'CTEENTERO', 'CTEFLOTANTE', 'CTETEXTO'
    )

reserved = { 'inicio_programa' : 'INICIO_PROGRAMA', 
             'fin_programa'    : 'FIN_PROGRAMA', 
             'inicio_funcion' : 'INICIO_FUNCION', 
             'fin_funcion'     : 'FIN_FUNCION', 
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
             'fin_si': 'FIN_SI',
             'entonces': 'ENTONCES',
             'si_no': 'SI_NO',
             'mintras': 'MIENTRAS',
             'fin_mientras': 'FIN_MIENTRAS',
             'hacer': 'HACER',
             'pintar': 'PINTAR',
             'no_pintar': 'NO_PINTAR',
             'lista': 'LISTA',
             'agregar': 'AGREGAR',
             'sacar': 'SACAR',
             'decir_al_usuario': 'DECIR_AL_USUARIO',
             'pedir_al_usuario': 'PEDIR_AL_USUARIO',
             'inicio_bloque': 'INICIO_BLOQUE',
             'fin_bloque': 'FIN_BLOQUE',
             'entero': 'ENTERO',
             'flotante': 'FLOTANTE',
             'texto': 'TEXTO'
              }

t_CTEENTERO              = r'[0-9]+'
t_CTEFLOTANTE            = r'[0-9]+\.[0-9]+ '
t_CTETEXTO               = r'"\"".+"\""'
t_PUNTOCOMA           = r';'
t_PARENTIZQ       = r'\('
t_PARENTDER      = r'\)'
t_IGUAL            = r'='
t_IGUAL_QUE            = r'=='
t_MAS              = r'\+'
t_MENOS             = r'-'
t_DIV          = r'\/'
t_MULT              = r'\*'
t_MENOR_QUE              = r'<'
t_MAYOR_QUE           = r'>'
t_DIFERENTE_QUE         = r'<>'
t_COMA             = r','

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

def p_program(t): 'program : INICIO_PROGRAMA A cuerpo FIN_PROGRAMA'
    pass
def p_A(t): 
    '''A : vars
           | empty'''
   pass

def p_vars(t): 
    '''vars : CREAR tipo ID PUNTOCOMA vars
           | empty'''
    pass

 
def p_cuerpo(t): 'cuerpo : B principal'
    pass
 
def p_B(t): 
    '''B : funcion B
           | empty'''
    pass
 
def p_funcion(t): 'funcion : INICIO_FUNCION variable ID parametros C REGRESA expresion FIN_FUNCION'
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
           | accion
           | accion_general'''
    pass
 
def p_asignacion(t): 'asignacion : ID IGUAL expresion PUNTOCOMA'
    pass
 
def p_expresion(t): 'expresion : exp F'
    pass
 
def p_F(t): 
    '''F : MAYOR_QUE exp
           | MENOR_QUE exp
           | DIFERENTE_QUE exp
           | IGUAL_QUE exp
           | empty'''
    pass
 
def p_exp(t): 'exp : termino G'
    pass
 
def p_G(t): 
    '''G : MAS termino
           | MENOS termino
           | empty'''
    pass
 
def p_termino(t): 'termino : factor H'
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


def I(t):
    '''I : MAS
           | MENOS
           | empty '''
pass
 
def varcte(t):
    '''varcte : ID
           | CTETEXTO
           | CTEFLOTANTE
           | CTEENTERO
           | llamada '''
pass
 
def llamada(t):
    'llamada : ID L'
pass
 
def L(t):
    '''L : PARAMETROS expresion M
           | empty  '''
pass
 
def M(t):
    '''M : COMA expresion M
           | empty  '''
pass
 
def condicion(t):
'condicion : SI expresion ENTONCES bloque J FIN_SI'
pass
 
def J(t):
'''J : SI_NO bloque
           | empty '''
pass
 
def ciclo(t):
'ciclo    : MIENTRAS expresion HACER bloque FIN_MIENTRAS'
pass
 
def io(t):
'''io : PEDIR_AL_USUARIO ID
           | DECIR_AL_USUARIO expresion '''
pass
 
def accion(t):
'accion   : tipo_accion O instruccion ID SEMICOlON'
 pass
 
def tipo_accion(t):
'''tipo_accion : lista
           | objeto '''
pass
 
def objeto(t):
'''objeto   : CREAR
           | DIBUJAR
           | BORRAR
           | GIRAR
           | PINTAR
           | DESPINTAR
           | MOVER '''
pass
 
def O(t):
'''O        : X expresion
           | Y expresion
           | DERECHA
           | IZQUIERDA
           | empty  '''
pass
 
def lista(t):
'''lista    : AGREGAR
           | SACAR
           | VER '''
pass
 
def accion_general(t):
'accion_general : ESPERA expresion'
pass
 
def bloque(t):
'bloque   : INICIO_BLOQUE K FIN_BLOQUE'
pass
 
def K(t):
'''K        : estatuto K
           | empty '''
pass
 
def tipo(t):
'''tipo     : svariable
           | LISTA '''
pass

def p_empty(t):
    'empty : '
    pass

def p_error(p):
    if p:
        print("Error de sintaxis en: '%s'" % p.value + p.type)
    else:
        print("Error de sintaxis")


entrada = open ("test-incorrecto2.in", "r");

import ply.lex as lex
lex.lex()
import ply.yacc as yacc
yacc.yacc()
yacc.parse(entrada.read())



