#!/usr/bin/env python
import socket
import threading
import time
import Interconnector as ic

port = 5050
host = '127.0.0.1'
statuses = ['Available', 'Unavailablex']
current_status = 0
wait_time_between_msg = 5
battery = 100

class LobbyClient():
	def __init__(self, host, port):
		self.name = socket.gethostname()
		self.host = host
		self.port = port

	def start_connection(self):
		threading.Thread(None, LobbyClient.connect_to_lobby, args=(self.host, self.port, self.name)).start()

	@staticmethod
	def connect_to_lobby(host, port, name):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			while True:
				try:
					s.connect((host, port))
					while True:
						msg = ic.RCPCMsg(name, statuses[current_status], battery)
						msg_str = msg.to_json()
						s.sendall(msg_str.encode('UTF-8'))

						data = s.recv(32)
						print(data)
						time.sleep(wait_time_between_msg)
				except:
					print('Waiting for connection...')
		print('Disconnected')

lc = LobbyClient()
lc.start_connection()
