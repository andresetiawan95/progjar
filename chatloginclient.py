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
	list_socket = [sys.stdin, sock] #memasukkan socket dirinya sendiri dan soccket server ke array list_socket
	
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
			command = msg1.split()
			length = len(command)
			if command[0]=="regist":
				if length > 1:
					print >>sys.stderr, 'Perintah yang anda ketikkan salah'
					print >>sys.stderr, 'Untuk registrasi, cukup ketik perintah: regist'					
				else:
					sys.stdout.write('Username : ')
					username = sys.stdin.readline()
					sys.stdout.write('Password : ')
					password = sys.stdin.readline()
					sock.send("regist "+username+" "+password)			
			elif command[0]=="login":
				if length > 1:
					print >>sys.stderr, 'Untuk login, cukup ketikkan perintah :login'
				else:
					sys.stdout.write('Username : ')
					userlogx = sys.stdin.readline()
					sys.stdout.write('Password : ')
					passlogx = sys.stdin.readline()
					sock.send("login "+userlogx+" "+passlogx)

			else:
				sock.send(msg1)

			sys.stdout.write('[Anda] ')
			sys.stdout.flush()
