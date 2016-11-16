#!/usr/bin/python3.5
"""
	By Seykotron
	TOPO (Twitter Observer Port Opener)
	Bot que escucha los mensajes privados de twitter para ejecutar acciones (por defecto abrir y cerrar puertos)
	en el servidor
"""
import re, json, time, threading, warnings,sys, subprocess
from Acciones import Acciones
from Parseador import Parseador
from TweetApp import TweetApp
from Bot import Bot

def cargarPreferencias():
	"""
		Carga las preferencias del programa
	"""
	with open('./config/topo.json') as data_file:
		datos = json.load(data_file)
		continuar = datos["continuar"]

	if continuar is not None:
		return continuar

def guardarPreferencias( datos ):
	"""
		Guarda el estado de las preferencias
		en principio solo contendra la variable continuar para poder detener el bot de manera limpia
	"""
	with open('./config/topo.json', 'w') as outfile:
		json.dump(datos, outfile)


if __name__ == "__main__":
	#Si recibo por argumento parar o stop paro el servicio que ya estuviera iniciado.
	if len(sys.argv) > 1 and ( sys.argv[1] == "parar" or sys.argv[1] == "stop" ):
		guardarPreferencias( { "continuar": False } )
	#Si recibo por argumento empezar o start empiezo el servicio
	elif len(sys.argv) > 1 and ( sys.argv[1] == "empezar" or sys.argv[1] == "start" ):
		bot = Bot()

		#Seteo la variable de continuar a verdadero para que funcione el loop infinito.
		continuar = True

		#Sobreescribo las preferencias por si estaban a false
		guardarPreferencias( { "continuar": continuar } )

		#print( parser.parsear( sys.argv[1] ) )

		#Bucle infinito
		while continuar:

			#Se ejecuta toda la logica del bot
			bot.tick()

			#Realizo el bucle infinitamente cada 15 segundos (para o exceder las peticiones de la api de twitter)
			time.sleep(15)
			continuar = cargarPreferencias()
	else:
		print("Bienvenido a TOPO (Twitter Observer PortKnocking Opener)")
		print("Uso: ")
		print("\tPara iniciar el bot: "+sys.argv[0]+" empezar|start")
		print("\tPara detener el bot activo:"+sys.argv[0]+" parar|stop")
		
