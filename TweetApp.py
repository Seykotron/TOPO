
import time, threading, tweepy, json

class TweetApp:
	"""
		Clase para manejar las notificaciones por twitter.
	"""

	def __init__(self ):
		"""
			Inicia la instancia de la clase con las variables necesarias para escribir.
		"""

		self.cargarJSON()

		self.auth = tweepy.OAuthHandler( self.twitter["cKey"], self.twitter["cSecret"] )
		self.auth.set_access_token( self.twitter["aToken"], self.twitter["aSecret"] )

		self.api = tweepy.API( self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True )

		self.listaSeguidores()



	def listaSeguidores(self):
		"""
			Rellena la lista de seguidores que se tiene
		"""

		self.listaSeguidores = []

		for friend in tweepy.Cursor(self.api.friends).items():
			self.listaSeguidores.append( friend.screen_name )

	def listar_mensajes_directos( self ):
		"""
			Devuelve una lisa con los mensajes recibidos en forma de diccionario
			{
				"id" : id_del_mensaje,
				"screen_name" : screen_name_del_sender,
				"text" : texto_del_mensaje
			}
		"""
		mensajes_recibidos = self.api.direct_messages( since_id = self.twitter["ultimoId"] )

		salida = []

		for mensaje in mensajes_recibidos:
			#obtengo el diccionario con los datos que me interesan
			objeto = { "id" : mensaje.id, "screen_name" : mensaje.sender_screen_name, "text" : mensaje.text }

			#Agrego el objeto a la salida
			salida.append( objeto )

			#Actualizo el fichero json para guardar el ultimo id leido.
			if mensaje.id > self.twitter["ultimoId"]:
				self.twitter["ultimoId"] = mensaje.id

				#Guardo los datos del fichero json
				self.guardarJSON()

		return salida

	def mensaje_directo( self, usuario, texto ):
		"""
			Manda un mensaje directo al usuario que le indiques. OJO el usuario debe estar siguiendote y tu a el.
		"""
		self.api.send_direct_message( screen_name = "@"+usuario, text = texto )

	def mensaje_directo_a_todos( self, texto ):
		"""
			Envia un mensaje directo a todas las cuentas que existan en la tabla de la bbdd "Notificaciones"
		"""
		listaUsuarios = self.getListaUsuarios()

		for usuario in listaUsuarios.keys():
			self.mensaje_directo( usuario, texto )

	def guardarJSON(self):
		"""
			Guarda los datos del fichero json
		"""
		with open('./config/twitter.json', 'w') as outfile:
			json.dump(self.twitter, outfile)

	def cargarJSON(self):
		"""
			Carga los datos del fichero json
		"""
		with open('./config/twitter.json') as data_file:
			self.twitter = json.load(data_file)
