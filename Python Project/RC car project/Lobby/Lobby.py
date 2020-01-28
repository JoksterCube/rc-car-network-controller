#!/usr/bin/env python
import socket
import threading
import time
import Interconnector as ic

host = ''
car_port = 5050
controller_port = 5060
backlog = 5

class LobbyServer():
	def __init__(self, host, car_port, controller_port):
		self.host = host
		self.car_port = car_port
		self.controller_port = controller_port
		self.__car_list = []
		self.__clients = []
		self.__stop = False

	def start_lobby(self, backlog=1):
		self.__stop = False
		threading.Thread(None, LobbyServer.__listen_for_car_connections, args=(self.host, self.car_port, backlog, self)).start()
		threading.Thread(None, LobbyServer.__listen_for_controller_connections, args=(self.host, self.controller_port, backlog, self)).start()
	
	def stop_lobby(self):
		self.__stop = True
	
	def is_stopping(self):
		return self.__stop

	def get_car_list(self):
		return self.__car_list

	def get_controller_list(self):
		return self.__clients

	def __update_car_list(self, addr, msg):
		self.__remove_from_car_list(addr)
		self.__car_list.append({'address': addr, 'data': msg})

	def __remove_from_car_list(self, addr):
		self.__car_list = [car for car in self.__car_list if car['address'] != addr]

	def __update_clients(self, addr, name):
		if self.__check_client(addr, name):
			return False
		else:
			self.__clients.append({'address': addr, 'name': name})
			return True
			
	def __check_client(self, addr, name):
		return len([client for client in self.__clients if client['address'] == addr and client['name'] == name]) > 0
		
	def __remove_clients(self, addr, name):
		self.__clients = [client for client in self.__clients if client['address'] != addr and client['name'] != name]

	@staticmethod
	def __listen_for_car_connections(host, port, backlog, parent):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((host, port))
			s.settimeout(1)
			s.listen(backlog)
			while not parent.is_stopping():
				try:
					conn, addr = s.accept()
					threading.Thread(None, LobbyServer.__new_lobby_car_client, addr, (conn, addr, parent)).start()
				except:
					pass

	@staticmethod
	def __listen_for_controller_connections(host, port, backlog, parent):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((host, port))
			s.settimeout(1)
			s.listen(backlog)
			while not parent.is_stopping():
				try:
					conn, addr = s.accept()
					threading.Thread(None, LobbyServer.__new_lobby_controller_client, addr, (conn, addr, parent)).start()
				except:
					pass
	
	@staticmethod
	def __new_lobby_car_client(conn, addr, parent):
		with conn:
			print('[CAR] Connected by', addr)
			while not parent.is_stopping():
				try:
					data = conn.recv(1024)
					if not data: break

					msg = ic.CarStatusMsg.from_json(data.decode('UTF-8'))
					parent.__update_car_list(addr, msg)
					conn.sendall(b'OK')
				except:
					break
		print('[CAR] Disconnected by', addr)
		parent.__remove_from_car_list(addr)

	@staticmethod
	def __new_lobby_controller_client(conn, addr, parent):
		with conn:
			print('[CLIENT] Connected by', addr)
			while not parent.is_stopping():
				try:
					name = conn.recv(32)
					if not name: break
					parent.__update_client(name.decode('UTF-8'))
					msg = ic.CarStatusMsg.list_to_json(parent.get_car_list())
					conn.sendall(msg.encode('UTF-8'))
				except:
					break
		print('[CLIENT] Disconnected by', addr)
		parent.__remove_clients(addr)

							   
ls = LobbyServer(host, car_port, controller_port)
ls.start_lobby(backlog)

i = 0
while True:
	print(i, ': ', ls.get_car_list())
	time.sleep(1)
	i += 1
ls.stop_lobby()