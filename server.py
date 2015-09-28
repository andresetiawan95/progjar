#Andre Setiawan 5113100013
import sys,select,socket
def send_message (socks, message):
#mengirim pesan kepada peer
	for socketz in socket_terbaca:
		if socketz != sock and socketz != socks : #mengirim pesan ke client lain, kecuali ke client yang mengirim pesan tsb
			try :
				socketz.send(message)
			except :
				socketz.close()
				socket_terbaca.remove(socketz)

socket_terbaca = [] #menyimpan daftar koneksi yang dapat dibaca
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(10)
socket_terbaca.append(sock) #memasukkan socket server kedalam daftar koneksi yang dapat dibaca

while True:
	read_socket,write_socket,socket_err = select.select(socket_terbaca,[],[]) #membaca seluruh koneksi yang dapat dibaca 
	
    	for socks in read_socket:
		if socks == sock: #jika master socket yang readable, maka ada koneksi baru yang masuk
			connection, client_address = sock.accept()
			socket_terbaca.append(connection) #client socket dimasukkan ke daftar koneksi yang dapat dibaca
			print "[%s: %s] terhubung ke server" % client_address
			send_message(connection, "\r"+"Seorang teman memasuki chat room\n")
		else : #jika client socket yang readable, maka server akan membaca pesan, dan dikirim ke client yang lain
			try:
				data = socks.recv(4096)
				if data:
					send_message(socks, "\r"+'[' + str(socks.getpeername()) + '] ' + data)
					
				else:
					if socks in socket_terbaca:
						send_message(socks,"Teman anda telah offline\n")
						socks.close()
						socket_terbaca.remove(socks)
			
			except: #error handling
				send_message(socks, "Teman anda telah offline\n")
				socket_terbaca.remove(socks)				
				continue
sock.close()	
