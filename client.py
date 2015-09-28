#Andre Setiawan 5113100013
import sys, socket, select

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connected to %s port %s' % server_address
sock.connect(server_address)

sys.stdout.write('[Anda] ')
sys.stdout.flush()
while True:
	list_socket = [sys.stdin, sock] #menerima daftar koneksi yg dapat dibaca di socket server dan dimasukkan kedalam list_socket
	
	read_socket,write_socket,socket_err = select.select(list_socket,[],[])
	for socks in read_socket:
		if socks == sock:
			data = socks.recv(4096)
			if data :
				sys.stdout.write(data)
				sys.stdout.write('[Anda] ')
				sys.stdout.flush()
			else :
				print '\nTerputus dari server'
				sys.exit()
		else :
			msg = sys.stdin.readline()
			sock.send(msg)
			sys.stdout.write('[Anda] ')
			sys.stdout.flush()
