# Worst Gross
import socket
s = socket.socket()
s.bind(('',54321))
s.listen(5)
conn, addr = s.accept()
data = conn.recv(1042)





# Gross simple
import socket 
s = socket.socket()
s.bind(('',54321))
s.listen(5)
while True:
	conn, addr = s.accept()
	conn.send(addr[0]+": "+conn.recv(1042))
	
	
	
# Gross multi-thread example
import socket
from thread import start_new_thread
s = socket.socket()
buff = 512
s.bind(('',54321))
s.listen(5)

def client_conn(conn, addr, buff):
	conn.send("Welcome to my server. Please send me something\r\n")
	While True:
		data = conn.recv(buff)
		reply = 'OK... ' + data
		if not data:
			break
		elif data.startswith('end'):
			conn.close()
		print addr[0] + ": ", data.strip()
		conn.send(reply)
	conn.close()
	
While True:
	conn, addr = s.accept()
	print "Connection Received from %s on port %s" %(addr[0], addr[1])
	start_new_thread(client_conn, (conn, addr, buff))
	
	