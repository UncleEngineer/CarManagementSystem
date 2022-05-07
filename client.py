import socket

serverip = '192.168.0.100'
port = 9000
buffsize = 4096

for i in range(10):
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))

	data = input('Send to Server: ')
	server.send(data.encode('utf-8'))

	data_server = server.recv(buffsize).decode('utf-8')
	print('Data from server: ', data_server)
	server.close()


