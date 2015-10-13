import sys,select,socket,string

def sendmessage (socks, message):
	try:
		socks.send(message)
	except:
		socks.close()
		if socks in socket_terbaca:
			socket_terbaca.remove(socks)

def register (socks, name, paswd):
	usr_test=0
	for alluser in akun:
		if alluser == name:
			usr_test=1
	if usr_test == 1:
		sendmessage (socks, "Username telah dipakai\n")
	else:
		akun.append(name)
		akun.append(paswd)
		sendmessage (socks, "Anda berhasil terdaftar\n")	

def loginusr (socks, name, paswd):
	usr_test=0
	log_test=0
	valid_login=0
	for alluser in user_list:
		if alluser == name:
			usr_test=1
		if alluser == socks:
			log_test=1
	if log_test == 1:
		sendmessage (socks, "Anda telah login.\n")
	elif usr_test == 1:
		sendmessage (socks, "Anda telah login.\n")
	else:
		for a in range (len(akun)):
			if akun[a] == name and akun[a+1] == paswd:				
				valid_login=1
		if valid_login==1:
			user_list.append(socks)
			user_list.append(name)
			sendmessage (socks, "Login sukses\n")				
		else:
			sendmessage (socks, "Username atau Password anda Salah\n")

def broadcastmessage (socks, message):
	for a in range (len(user_list)):
		if user_list[a] != sock and user_list[a] != socks and a%2==0:
			try:
				user_list[a].send(message)
			except:
				user_list[a].close()
				if user_list[a] in socket_terbaca:
					socket_terbaca.remove(user_list[a])
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
user_list = []
akun = []
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
			broadcastmessage(connection, "\r"+"Seorang teman memasuki chat room\n")
		else : #jika client socket yang readable, maka server akan membaca pesan, dan dikirim ke client yang lain
			try:
				data = socks.recv(4096)
				if data:
					command = data.split()
					length = len(command)
					if command[0]=="regist":
						register(socks, str(command[1]), str(command[2]))					
					elif command[0]=="login":
						loginusr(socks, str(command[1]), str(command[2]))
					elif command[0]=="list-user":
						cek_login=0
						
						for a in range (len(user_list)):
							if user_list[a]==socks:
								cek_login=1
						if cek_login==0:
							sendmessage(socks,"Anda harus login terlebih dahulu\n")
						else:
							listuser = ""
							for a in range(len(user_list)):
								if a%2==1: #meminta nama username tersimpan di indeks ganjil array user_list
									listuser += " "
									listuser += str(user_list[a])
									listuser += ","
							sendmessage(socks, "\r" + "List User : " + listuser + "\n")
					elif command[0]=="send-to":
						cek_login=0
						user_now=""
						for a in range (len(user_list)):
							if user_list[a]==socks:
								user_now=user_list[a+1] #mengambil nama user
								cek_login=1
						if cek_login==0:
							sendmessage(socks,"Anda harus login terlebih dahulu\n")
						else:
							your_msg=""
							for a in range (len(command)):
								if a>1: #indeks array command yang lebih dari 1 merupakan isi pesan
									if your_msg:
										your_msg += " "
										your_msg += str(command[a])
									else:
										your_msg += str(command[a]) 
							for a in range (len(user_list)):
								if user_list[a]==command[1]:
									sendmessage(user_list[a-1], "\r"+"Pesan pribadi dari "+'['+user_now+'] ' + your_msg + "\n")
					else:
						cek_login=0
						user_now=""
						for a in range (len(user_list)):
							if user_list[a]==socks:
								user_now=user_list[a+1]
								cek_login=1
						if cek_login==0:
							sendmessage(socks, "Anda harus login terlebih dahulu\n")
						else:
							your_msg=""
							for a in range (len(command)):
								if your_msg:
									your_msg += " "
									your_msg += str(command[a])
								else:
									your_msg += str(command[a])
							
							broadcastmessage(socks, "\r" + '['+user_now+'] ' + your_msg + "\n")
						
#send_message(socks, "\r"+'[' + str(socks.getpeername()) + '] ' + data)
				else:
					if socks in socket_terbaca:
						broadcastmessage(socks,"Teman anda telah offline\n")
						socks.close()
						socket_terbaca.remove(socks)
			
			except: #error handling
				send_message(socks, "Teman anda telah offline\n")
				socket_terbaca.remove(socks)				
				continue
sock.close()	
