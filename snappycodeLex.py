# snappycodeLex.py

#Definicion de los Tokens
import sys
import ply.lex as lex

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

lex.lex()