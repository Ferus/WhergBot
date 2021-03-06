#!/usr/bin/env python
import requests
import json
import re
from .Settings import Settings
#https://github.com/KevinLi/PyFileServ
#Uses API link to get data


def Get(url, id):
	try:
		req = requests.get("{0}/api?file={1}".format(url, id))
	except requests.ConnectionError:
		return None
	if not req.status_code == 200:
		return None
	data = json.loads(req.text)
	return data

def Format(data):
	s = "\x02[PyFileServ]\x02"
	s += " File \x02{0}\x02".format(data['filename'])
	s += " (\x02{0}\x02)".format(data['mimetype'])
	s += " [\x02{0}\x02]".format(data['timestamp'])
	s += " Views: \x02{0}\x02".format(data['views'])
	return s


class Main(object):
	def __init__(self, Name, Parser):
		self.__name__ = Name
		self.Parser = Parser
		self.IRC = self.Parser.IRC

	def Parse(self, data):
		ids = []
		for x in Settings.get('links'):
			for y in re.findall(x, ' '.join(data[3:])):
				url, imgid = y.rsplit("/", 1)
				ids.append((url, imgid))
		ids = list(set(ids)) # Remove Dupes
		for x in ids:
			info = Get(x[0], x[1])
			if not info:
				pass
			else:
				self.IRC.say(data[2], Format(info))

	def Load(self):
		regex = "(" + "|".join(x for x in Settings.get("links")) + ")"
		self.Parser.hookCommand('PRIVMSG', self.__name__, {regex: self.Parse})

	def Unload(self):
		pass
	def Reload(self):
		pass
