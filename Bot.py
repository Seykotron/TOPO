"""
	By Seykotron

	Bot para el topo, aqui se maneja todo lo del bucle principal
"""
import re, json, time, threading, warnings,sys, subprocess
from Acciones import Acciones
from Parseador import Parseador
from TweetApp import TweetApp


class Bot:

	def __init__(self):
		#Inicializo el parseador
		self.parser = Parseador()
		#Inicializo la clase de twitter
		self.ta = TweetApp()

	def tick(self):
		"""
			Este metodo es llamado cada vez que el bucle principal da una vuelta

			Se solicita una lista de mensajes privados recibidos, y se actua para cada uno de ellos
		"""

		#Obtengo la lista
		mensajes = self.ta.listar_mensajes_directos()

		#Ordeno la lista por id, para tenerlos ordenados de mas viejo a mas nuevo
		mensajes = sorted(mensajes, key=lambda k: k['id'])

		#Recorro la lista mensaje a mensaje
		for mensaje in mensajes:
			respuesta = self.parser.parsear(mensaje["text"])

			#Si hay una respuesta para el mensaje recibido, se le responde.
			if respuesta is not None:
				self.ta.mensaje_directo( mensaje["screen_name"], respuesta )
