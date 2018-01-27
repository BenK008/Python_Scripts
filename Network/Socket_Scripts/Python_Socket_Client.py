import socket
import subprocess
import struct
import os
import argparse
import errno
import time

class Client_Socket:
	def __init__(self, _address = "192.168.0.3", _port = 54321, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((_address, _port))
		else:
			self.sock = sock

	#def Client_Connect(self, _address = "10.3.1.182", _port = 54321):
		#self.sock = self.sock.connect((_address, _port))

	def Client_Send_Data(self, _msg):
                _msglen = len(_msg)
		msg_to_send = struct.pack('>I', _msglen) + _msg
                if self.sock is not None:
                    self.sock.send(msg_to_send)
                else:
                    print "Send Failed: Socket Closed"

	def Client_Recv_All(self, sock, n):
	    data = ""
	    while len(data) < n:
                try:
                    p = sock.recv(n - len(data), 0x40)
	            if not p:
	                print "Connection Closed"
                        sock.close()
                        break
                    else:
	                data += p
		        return data
                except socket.error, e:
                    if e.args[0] == errno.EWOULDBLOCK:
                        time.sleep(1)
                    else:
                        print e
                        break

	def Client_Receive_Data(self):
            _received_message = []
	    _flag = 0
	    _flag = self.Client_Recv_All(self.sock, 4)
	    if not _flag:
                return None
	    _message_length = struct.unpack('>I', _flag)[0]
	    _received_message.append(self.Client_Recv_All(self.sock, _message_length))
            print str(_message_length)
            for i in _received_message:
                print i

	def Client_Interact(self):
            while True:
		data = raw_input("Ben_Py_Shell#: ")
		self.Client_Send_Data(data)
		if 'exit' in data or '__blow_up' in data:
		    self.sock.close()
		    break
                else:
                    self.Client_Receive_Data()

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
		client_socket.Client_Interact()
	else:
		print _server + " is down."
