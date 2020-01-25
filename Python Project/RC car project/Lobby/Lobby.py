#!/usr/bin/env python
import socket
import threading
import time

port = 5050
host = ''
backlog = 5

class LobbyServer():
	def __init__(self, port=port, host=host):
		self.port = port
		self.host = host
		self.car_list = []
		self.shutting_down = False

	def start_lobby(self, b=backlog):
		threading.Thread(None, LobbyServer.listen_for_connections, args=(self.host, self.port, b, self)).start()
	
	def shut_down(self):
		self.shutting_down = True

	@staticmethod
	def listen_for_connections(host, port, b, parent):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((host, port))
			s.settimeout(1)
			s.listen(b)
			while not parent.shutting_down:
				try:
					conn, addr = s.accept()
					parent.car_list.append({'address': addr, 'name': '', 'status':''})
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
					print(data)
					if not data: 
						break
					conn.sendall(data)
				except:
					print('Disconnected by', addr)
					break
		parent.car_list.remove(addr)

							   
ls = LobbyServer()
ls.start_lobby()
i = 0
while True:
	print(i, ': ', ls.car_list)
	time.sleep(1)
	i += 1
ls.shut_down()