import socket
import thread
import subprocess
import struct
import os
import argparse
import time

class Client_Socket:
	def __init__(self, _address = "192.168.0.3", _port = 54321, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock = self.sock.connect((_address, _port))
		else:
			self.sock = sock
		
	#def Client_Connect(self, _address = "10.3.1.182", _port = 54321):
		#self.sock = self.sock.connect((_address, _port))
	
	def Client_Send_Data(self, _msg):
		_bytes = 0
		_msg_length = len(self._msg)
		while _bytes < _msg_length:
			msg_sent = self.sock.send(msg[_bytes:])
			if msg_sent == 0:
				raise RuntimeError("Socket Closed")
			_bytes += len(msg_sent)
		msg_to_send = struct.pack('>I', len(msg_sent)) + msg_sent
		print msg_to_send
		self.sock.send(msg_to_send)	

	def Client_Recv_All(self, n):
		data = ""
		while len(data) < n:
			p = self.sock.recv(n - len(data))
			if not p:
				return None
			data += p
		return data
			
	def Client_Recieve_Data(self):
		_bytes = 0
		while True:
			_message_length = self.Client_Recv_All(4)
			if not _message_length:
				return None
			mlen = struct.unpack('>I', _message_length)[0]
			self.receive_message = self.Client_Recv_All(self.sock, mlen)
			output = self.receive_message
			
	def Client_Interact(self, conn):
		while conn is not None:
			data = raw_input("Ben_Py_Shell#: ")
			self.Client_Send_Data(data)
			if data.startswith('exit') or data.startswith('__blow_up'):
				self.sock.close()
			else:
				self.Client_Recieve_Data()
			
# Instantiating the parser to establish cmdline arguments and help data
parser = argparse.ArgumentParser ( description = "Python socket client" )
parser.add_argument( "-s", "--server", help = "Server to connect to", required = True )
parser.add_argument( "-p", "--port", help = "Port to connect to", required = True )
args = parser.parse_args()
			
if __name__ == "__main__":
	_server = str(args.server)
	_port = int(args.port)
	#response = os.system("ping -c 1 " + _server + " >/dev/null 2>&1")
	response = 0
	if response == 0:
		client_socket = Client_Socket(_server, _port)
		#client_socket.Client_Connect(_server, _port)
		client_socket.Client_Interact(client_socket.sock)
	else:
		print _server + " is down."
	
	
	
			