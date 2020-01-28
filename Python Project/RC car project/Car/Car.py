#!/usr/bin/env python
import socket
import threading
import time
import Interconnector as ic

host = '127.0.0.1'
port = 5050
statuses = ['Available', 'Unavailablex']
current_status = 0
wait_time_between_msg = 5
battery = 100

class LobbyClient():
	def __init__(self, host, port):
		self.name = socket.gethostname()
		self.host = host
		self.port = port
		self.__stop = False

	def start_connection(self, wait_time):
		self.__stop = False
		threading.Thread(None, LobbyClient.__connect_to_lobby, args=(self.host, self.port, self.name, self, wait_time)).start()

	def is_stopping(self):
		return self.__stop

	def stop_connection(self):
		self.__stop = True

	@staticmethod
	def __connect_to_lobby(host, port, name, parent, wait_time=1):
		while not parent.is_stopping():
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				while not parent.is_stopping():
					try:
						s.connect((host, port))
						print('Connected to', (host, port))
						break
					except:
						pass

				while not parent.is_stopping():
					try:
						msg = ic.CarStatusMsg(name, statuses[current_status], battery)
						msg_str = msg.to_json()
						s.sendall(msg_str.encode('UTF-8'))

						data = s.recv(32)
						if not data: 
							print('Status update: NONE')
							break

						print('Status update: {}'.format(data.decode('UTF-8')))
						time.sleep(wait_time)
					except:
						break
					
				print('Disconnected from', (host, port))

lc = LobbyClient(host, port)
lc.start_connection(wait_time_between_msg)