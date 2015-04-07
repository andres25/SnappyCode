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

class Memoria(object):
  def __init__(self):
		self.globales = Memoria_sub()
		self.locales = Memoria_sub()
		self.temporales = Memoria_sub()
		self.constantes = Memoria_sub()
		
class Memoria_sub(object):
	def __init__(self):
		self.entero = [ ]
		self.flotante = [ ]
		self.texto = [ ]
		self.booleano = [ ]

	def new_entero(self, celda):
		self.entero.append(celda)

	def new_flotante(self, celda):
		self.flotante.append(celda)

	def new_texto(self, celda):
		self.texto.append(celda)

	def new_booleano(self, celda):
		self.booleano.append(celda)

class Memoria_celda(object):
	def __init__(self, _dir, value):
		if _dir>=0:
			self.direccion = _dir
			self.valor = value
		else:
			print "No existe la direccion de memoria"
			sys.exit()
	