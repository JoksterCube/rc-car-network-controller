#!/usr/bin/env python
import json

class CarStatusMsg:
	def __init__(self, name, status, battery):
		self.name = name
		self.status = status
		self.battery = battery

	def __str__(self):
		return 'Name: {}; status: {}; battery: {}%'.format(self.name, self.status, self.battery);

	def __repr__(self):
		return self.__str__()

	def dictionary(self):
		return {'name': self.name, 'status': self.status, 'battery': self.battery}

	def to_json(self):
		return json.dumps(self.dictionary())

	@staticmethod
	def from_json(json_str):
		x = json.loads(json_str)
		return CarStatusMsg(x['name'], x['status'], x['battery'])

	@staticmethod
	def list_to_json(msg_list):
		msg_dicts = [msg.dictionary() for msg in msg_list]
		return json.dumbs(msg_dicts)
