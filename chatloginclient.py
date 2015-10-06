#Andre Setiawan 5113100013
import sys, socket, select, string

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
			msg1 = sys.stdin.readline()
			command = string.split(msg1[:-1])
			length = len(command)
			if command[0]=="login":
				if length < 2:
					print('Anda belum memasukkan username')
				elif length > 2:
					print('Input tidak valid')
				else:
					sock.send(msg1)
			elif command[0]=="list-user":
				if length > 1:
					print('Wrong command')
				else:
					sock.send(msg1)
			elif command[0]=="send-to":
				if length < 3:
					print('Wrong command')
				else:
					sock.send(msg1)
			else:
				sock.send(msg1)

			sys.stdout.write('[Anda] ')
			sys.stdout.flush()
