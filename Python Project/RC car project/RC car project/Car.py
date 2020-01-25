#!/usr/bin/env python
import socket
import threading
import time

port = 5050
host = '127.0.0.1'

class LobbyClient():
	def __init__(self, port=port, host=host):
		self.name = socket.gethostname()
		self.port = port
		self.host = host

	def start_connection(self):
		threading.Thread(None, LobbyClient.connect_to_lobby, args=(self.host, self.port, self.name)).start()

	@staticmethod
	def connect_to_lobby(host, port, name):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((host, port))
			s.sendall(name.encode('UTF-8'))
			data = s.recv(1024)
			print('Received', repr(data))
		print('Disconnected')


lc = LobbyClient()
lc.start_connection()


