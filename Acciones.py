"""
	By Seykotron
	Clase en la que guardar los métodos que contendran las acciones a realizar.
"""
import re, json, time, threading, warnings,sys, subprocess

class Acciones:

	def __init__(self, parseador):
		self.parseador = parseador

	def listarAcciones(self):
		"""
			Metodo para listar las acciones
		"""
		aux = "Lista de acciones:\n"
		for accion in self.parseador.listaAcciones.keys():
			aux += "\t"+accion+"\n"
		return aux

	def estaBotActivo(self):
		"""
			Metodo que dice si esta el bot activo o no
		"""
		output = subprocess.run("pgrep Blogabet.py", shell=True, stdout=subprocess.PIPE,
                        universal_newlines=True)

		if output is None:
			return "No esta activo el bot."
		else:
			return "El bot esta funcionando."

	def abrirPuerto(self, nPuerto):
		"""
			Metodo que abre un puerto específico
		"""

		output = subprocess.run("sudo iptables -I INPUT 1 -p tcp --dport "+str(nPuerto)+" -j ACCEPT", shell=True, stdout=subprocess.PIPE,
                        universal_newlines=True)
		return "Abriendo el puerto "+str(nPuerto)

	def cerrarPuerto(self, nPuerto ):
		"""
			Metodo que cierra un puerto específico
		"""

		return "Cerrando el puerto "+str(nPuerto)

	def eliminarIptables(self ):
		"""
			Metodo que elimina las iptables
		"""

		return "Iptables eliminadas."

	def listarPuertos(self):
		"""
			Metodo que lista los puertos que estan abiertos por iptables
		"""

		#Variables reservadas para el output de los comandos del sistema.
		src = ""
		dst = ""
		prt = ""

		#Ejecuto el comando del sistema para obtener la 4a columna de la salida de las iptables
		output = subprocess.run("iptables -nL INPUT | awk '{print $4}'", shell=True, stdout=subprocess.PIPE,
                        universal_newlines=True)
		if output is not None:
			#Si el resultado no es nulo, guardo esa informacion en la variable src
			src = str(output.stdout)

		#Ejecuto el comando del sistema para obtener la 5a columna de la salida de las iptables
		output = subprocess.run("iptables -nL INPUT | awk '{print $5}'", shell=True, stdout=subprocess.PIPE,
                        universal_newlines=True)
		if output is not None:
			#Si el resultado no es nulo, guardo esa informacion en la variable dst
			dst = str(output.stdout)

		#Ejecuto el comando del sistema para obtener la 7a columna de la salida de las iptables
		output = subprocess.run("iptables -nL INPUT | awk '{print $7}'", shell=True, stdout=subprocess.PIPE,
                        universal_newlines=True)
		if output is not None:
			#Si el resultado no es nulo, guardo esa informacion en la variable prt
			prt = str(output.stdout)

		#inicializo la lista de los puertos que estan abiertos
		puertosAbiertos = []

		#Divido las cadenas de texto linea a linea para iterarlas mejor
		listaSrc = src.split("\n")
		listaDst = dst.split("\n")
		listaPrt = prt.split("\n")

		#Si todas las salidas han tenido mas de dos lineas de output
		if len(listaSrc) > 2 and len(listaDst) > 2 and len(listaPrt) > 2:
			#Las recorro obviando las tres primeras (que son cabeceras) y la ultima (que esta vacia por un \n que hay)
			for i in range(3,len(listaSrc)-1):
				#Agrego a la lista de puertos abiertos un diccionario con la informacion util
				puertosAbiertos.append( { "src": listaSrc[i], "dst": listaDst[i], "port": listaPrt[i] } )

		#Inicializo la variable salida
		salida = ""

		#Recorro la lista de los puertos abiertos
		for puerto in puertosAbiertos:

			ipOrigen = ""
			ipDestino = ""

			#Si la ip origen es distinta de 0.0.0.0/0 entonces es que existe una ip origen
			if puerto["src"] != "0.0.0.0/0":
				ipOrigen = " desde la ip origen "+puerto["src"]

			#Si la ip destino es distinta de 0.0.0.0/0 entonces es que existe una ip destino
			if puerto["dst"] != "0.0.0.0/0":
				ipDestino = " a la ip destino "+puerto["dst"]

			#Obtengo el numero del puerto (el output es del estilo prt:1234 y solo me interesa lo que esta despues de los :)
			pnumero = puerto["port"].split(":")
			pnumero = pnumero[1]

			#Agrego la linea a la salida
			salida += "El puerto "+pnumero+" está abierto"+ipOrigen+ipDestino+"\n"

		return salida
		
