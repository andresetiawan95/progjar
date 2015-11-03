import sys
import socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the port
server_address = ('localhost', 8080)
sock.bind(server_address)
sock.listen(10)
print >>sys.stderr, 'starting up on %s port %s' % server_address
# Listen for incoming connections
while True:
    	# Wait for a connection
    	print >>sys.stderr, 'waiting for a connection'
    	connection, client_address = sock.accept()
    	print >>sys.stderr, 'connection from', client_address
    	# Receive the data in small chunks and retransmit it
    	# while True:
        data = connection.recv(2048)  	
	respon = "Sukses Menyambung ke Web Server"
	print data
	connection.send(respon)
	# Clean up the connection
	connection.close()