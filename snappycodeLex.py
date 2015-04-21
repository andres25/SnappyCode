# snappycodeLex.py

#Definicion de los Tokens
import sys
import ply.lex as lex

tokens = ( 'INICIOPROGRAMA', 'FINPROGRAMA', 'INICIOFUNCION', 'FINFUNCION', 'REGRESA', 'PARAMETROS',
    'CREAR','BORRAR','ID','TRUE','FALSE', 'INICIOPRINCIPAL', 'FINPRINCIPAL',
    'MOVER','GIRARDERECHA','GIRARIZQUIERDA', 'SI','FINSI' ,'ENTONCES',
    'SINO','MIENTRAS','FINMIENTRAS','HACER','LISTA', 'IGUAL', 'IGUALQUE' , 'MAYORQUE' , 'MENORQUE', 'DIFERENTEQUE', 
    'PINTAR', 'DESPINTAR', 'DECIRALUSUARIO', 'PEDIRALUSUARIO', 'INICIOBLOQUE', 'FINBLOQUE', 'MAS',
    'MENOS','COMA', 'MULT', 'DIV', 'PUNTOCOMA','PARENTIZQ','PARENTDER', 'ENTERO', 'FLOTANTE', 'TEXTO', 
    'CTEENTERO', 'CTEFLOTANTE', 'CTETEXTO', 'MAYORIGUAL', 'MENORIGUAL', 'BOOLEANO', 'CORCHETEIZQ', 'CORCHETEDER'
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
             'REGRESA'   : 'REGRESA',
             'regresa'   : 'regresa',
             'crear'     : 'CREAR', 
             'CREAR'     : 'CREAR',
             'borrar'    : 'BORRAR',
             'BORRAR'    : 'BORRAR',
             'mover'    : 'MOVER',
             'MOVER'    : 'MOVER',
             'girarderecha'    : 'GIRARDERECHA',
             'GIRARDERECHA'    : 'GIRARDERECHA',
             'girarizquierda'    : 'GIRARIZQUIERDA',
             'GIRARIZQUIERDA'    : 'GIRARIZQUIERDA',
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
             'BOOLEANO': 'BOOLEANO',
             'booleano': 'BOOLEANO',
             'TRUE': 'TRUE',
             'true': 'TRUE',
             'FALSE': 'FALSE',
             'false': 'FALSE',
              }

t_CTETEXTO               = r'"\"".+"\""'
t_PUNTOCOMA              = r';'
t_PARENTIZQ              = r'\('
t_PARENTDER              = r'\)'
t_CORCHETEIZQ              = r'\['
t_CORCHETEDER              = r'\]'
t_IGUAL                  = r'='
t_IGUALQUE               = r'=='
t_MAS                    = r'\+'
t_MENOS                  = r'-'
t_DIV                    = r'\/'
t_MULT                   = r'\*'
t_MENORQUE               = r'<'
t_MAYORQUE               = r'>'
t_DIFERENTEQUE           = r'<>'
t_MAYORIGUAL             = r'>='
t_MENORIGUAL             = r'<='
t_COMA                   = r','
t_TRUE                   = r'[1]'
t_FALSE                  = r'[0]'

t_ignore                 = " \t"

def t_ID(t):
    r'[A-Za-z]+[A-Za-z0-9]*'
    t.type = reserved.get(t.value,"ID")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_CTEFLOTANTE(t):
    r'-?\d+\.\d*(e-?\d+)?'
    t.value = float(t.value)
    return t    

def t_CTEENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Caracter no valido'%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()