from Packet import *

import socket
import sys
import os

def usage():
	print """Usage: python %s <Cmd-Type> """ % sys.argv[0] 
	sys.exit(0)

#For data node
def register(meta_ip, meta_port, data_ip, data_port):
	"""Creates a connection with the metadata server and
	   register as data node
	"""

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
	    sock.connect ((meta_ip, meta_port))
	except socket.error, e:
	    print "Could not connect with server.\n %s"%e
	    sys.exit(1)
	print "Connected to metadata server."

	try:
		response = "NAK"
		sp = Packet()
		while response == "NAK":
			sp.BuildRegPacket(data_ip, data_port)
			sock.sendall(sp.getEncodedPacket())
			response = sock.recv(1024)

			if response == "ACK":
				print "Registration Successful"

			if response == "DUP":
				print "Duplicate Registration"

		 	if response == "NAK":
				print "Registratation ERROR"

	finally:
		sock.close()

#For list of files
def client(ip, port):

	# Contacts the metadata server and ask for list of files.
		# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
	    sock.connect ((ip, port))
	except socket.error, e:
	    print "Could not connect with server.\n %s"%e
	    sys.exit(1)
	print "Connected to metadata server."

	try:
		response = "NAK"
		sp = Packet()
		while response == "NAK":
			sp.BuildListPacket()
			sock.sendall(sp.getEncodedPacket())
			response = sock.recv(1024)

			if response != "NAK":	
				sp.DecodePacket(response)
				lfiles = sp.getFileArray()

				if not lfiles:
					print "There are no files."
				else:
					for i in lfiles:
						print i[0], str(i[1]) + " Bytes"

	finally:
		sock.close()


if __name__ == "__main__":

	META_PORT = 8000
	cmd = sys.argv[1]

	if len(sys.argv) != 2:
		usage()

	# Simulating data node register
	if   cmd == "reg":

		HOST = 'localhost'
		PORT = 8001


		register("localhost", META_PORT, HOST, PORT)

	# Simulating list request
	elif cmd == "list":
		client("localhost", META_PORT)



