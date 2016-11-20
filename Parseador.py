"""
	By Seykotron
	Clase que maneja y parsea la entrada,
"""
import json, re, imp
from Acciones import Acciones

class Parseador:

	def __init__(self):
		self.acciones = Acciones(self)
		self.cargarListaAcciones()

	def cargarListaAcciones(self):
		"""
			Cargo la lista de acciones del fichero json
		"""
		with open('./config/listaAcciones.json') as data_file:
			self.listaAcciones = json.load(data_file)

	def parsear(self, username, frase ):
		"""
			Este metodo parsea la frase que le llegue y devuelve una salida en funcion de la frase de entrada
			en caso de que coincida con sus acciones
		"""

		#Recargo las acciones por si hubieran cambiado
		fp, pathname, description = imp.find_module("Acciones")
		imp.load_module("%s.%s" % ("Acciones", "Acciones"), fp, pathname, description)
		self.acciones = Acciones(self)

		#Recargo la lista de acciones
		self.cargarListaAcciones()

		for keyAccion in self.listaAcciones.keys():
			accion = self.listaAcciones[keyAccion]
			match = re.search( accion["regexp"], frase )
			if match:
				if hasattr(self.acciones, accion["accion"] ):
					if len(accion["grupos"]) == 1 and accion["grupos"][0] == -1:
						return getattr(self.acciones, accion["accion"])(username)
					elif len(accion["grupos"]) == 1:
						variable = match.group( accion["grupos"][0] )
						return getattr(self.acciones, accion["accion"])( username, variable )
					elif len(accion["grupos"]) > 1:
						aux = []
						for n in accion["grupos"]:
							aux.append = match.group( n )
						return getattr(self.acciones, accion["accion"])( username, aux )
				break
