###############################################################################
#
# Filename: mds_db.py
# Author: Jose R. Ortiz and ... (hopefully some students contribution)
#
# Description:
# 	List client for the DFS
#



import socket
import sys

from Packet import *

def usage():
	print """Usage: python %s <server>:<port, default=8000>""" % sys.argv[0] 
	sys.exit(0)

def client(ip, port):

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

	if len(sys.argv) < 2:
		usage()

	ip = None
	port = None 
	server = sys.argv[1].split(":")
	if len(server) == 1:
		ip = server[0]
		port = 8000
	elif len(server) == 2:
		ip = server[0]
		port = int(server[1])

	if not ip:
		usage()

	client(ip, port)
