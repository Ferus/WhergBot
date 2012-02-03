#!/usr/bin/env python

import Core
from threading import Timer

nick = 'WhergBot'
real = 'WhergBot [Ferus]'
ident = 'Wherg'
#channels = ['#hacking', '#lobby' ,'#4chon' ,'#circlejerk' , '#games', "#h"]
channels = ['#h']
owner = ['Ferus', 'anonymous@the.interwebs', 0]

server = 'opsimathia.datnode.net'
#proxy = ("127.0.0.1", 3125, "socks5")
proxy = None
ssl = True
if ssl:
	port = 6697
else:
	port = 6667

if __name__ == '__main__':
	try:
		WhergBot = Core.Bot(nick, real, ident, owner, ssl, proxy=proxy)
		WhergBot.Connect(server=server, port=port)
		if WhergBot.Nickserv.password != '':
			_p = Timer(3, WhergBot.Identify, ())
			_p.daemon = True
			_p.start()
		_t = Timer(5, WhergBot.irc.join, (",".join(channels),))
		_t.daemon = True
		_t.start() 

		while WhergBot.irc._isConnected:
			Msg = WhergBot.irc.recv()
			WhergBot.Parse(Msg)
			
	except KeyboardInterrupt:
		print("\n* [Core] Interrupt Caught; Quitting!")
		WhergBot.p.command.Quit("KeyboardInterrupt Caught!")
