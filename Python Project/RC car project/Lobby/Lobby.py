#!/usr/bin/env python
import socket
import threading
import time
import Interconnector as ic

port = 5050
host = ''
backlog = 5

class LobbyServer():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.car_list = []
		self.shutting_down = False

	def start_lobby(self, b=1):
		threading.Thread(None, LobbyServer.listen_for_connections, args=(self.host, self.port, b, self)).start()
	
	def shut_down(self):
		self.shutting_down = True
	
	def update_list(self, addr, msg):
		self.remove_list(addr)
		self.car_list.append({'address': addr, 'data': msg})

	def remove_list(self, addr):
		self.car_list = list(filter(lambda car: car['address'] != addr, self.car_list))

	@staticmethod
	def listen_for_connections(host, port, b, parent):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((host, port))
			s.settimeout(1)
			s.listen(b)
			while not parent.shutting_down:
				try:
					conn, addr = s.accept()
					threading.Thread(None, LobbyServer.new_lobby_client, addr, (conn, addr, parent)).start()
				except:
					pass
	
	@staticmethod
	def new_lobby_client(conn, addr, parent):
		with conn:
			print('Connected by', addr)
			while True:
				try:
					data = conn.recv(1024)
					if not data: break
					conn.sendall(b'OK')

					msg = ic.RCPCMsg.from_json(data.decode('UTF-8'))
					parent.update_list(addr, msg)
				except:
					print('Disconnected by', addr)
					break
		parent.remove_list(addr)
							   
ls = LobbyServer(host, port)
ls.start_lobby(backlog)

i = 0
while True:
	print(i, ': ', ls.car_list)
	time.sleep(1)
	i += 1
ls.shut_down()