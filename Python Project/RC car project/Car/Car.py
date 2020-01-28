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
		self.stop = False

	def start_connection(self, wait_time):
		self.stop = False
		threading.Thread(None, LobbyClient.connect_to_lobby, args=(self.host, self.port, self.name, self, wait_time)).start()

	def stop_connection(self):
		self.stop = True

	@staticmethod
	def connect_to_lobby(host, port, name, parent, wait_time=1):
		while not parent.stop:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				while not parent.stop:
					try:
						s.connect((host, port))
						print('Connected to', (host, port))
						while not parent.stop:
							msg = ic.RCPCMsg(name, statuses[current_status], battery)
							msg_str = msg.to_json()
							s.sendall(msg_str.encode('UTF-8'))

							data = s.recv(32)
							print('Status update: {}'.format(data.decode('UTF-8')))
							time.sleep(wait_time)
					except socket.error as exc:
						if exc.errno == 10061:
							print('Waiting for connection...')
							continue
						elif exc.errno in [10054, 10056]:
							print('Disconnected from', (host, port))
						else:
							print(exc)
						break
				print('Stopping')

lc = LobbyClient(host, port)
lc.start_connection(wait_time_between_msg)


