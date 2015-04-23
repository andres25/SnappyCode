#globales
EnteroGlobal = 0
FlotanteGlobal = 1000
TextoGlobal = 2000
BooleanGlobal = 3000

#locales
EnteroLocal=4000
FlotanteLocal=5000
TextoLocal=6000
BooleanLocal=7000

#Temporales
EnteroTemporal=8000
FlotanteTemporal=9000
TextoTemporal=10000
BooleanTemporal=11000

#Constantes
EnteroConstante=12000
FlotanteConstante=13000
TextoConstante=14000
BooleanConstante=15000

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
    return memoria

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
    return memoria

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
    return memoria

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
    return memoria