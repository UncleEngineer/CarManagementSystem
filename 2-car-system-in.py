import socket
from datetime import datetime
############ADRESS##############
serverip = '192.168.0.100'
port = 9000
buffsize = 4096

while True:
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))

	# - บันทึกข้อมูลรถ ยี่ห้อ สี ป้ายทะเบียน บัตร
	info = {'brand':{'q':'Brand: ','value':''},
			'color':{'q':'Color: ','value':''},
			'plate':{'q':'Plate: ','value':''},
			'card':{'q':'Card: ','value':''}}
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	# data = input('Send to Server: ')

	for k,v in info.items():
		d = input(v['q'])
		info[k]['value'] = d

	text = ''
	print(info)

	for v in info.values():
		text += v['value'] + '|'

	text += timestamp

	print(text)

	server.send(text.encode('utf-8'))
	data_server = server.recv(buffsize).decode('utf-8')
	print('Data from server: ', data_server)
	server.close()








'''
[2]-car-system-in.py
	- client-1.py
	(function)
		- บันทึกข้อมูลรถ ยี่ห้อ สี ป้ายทะเบียน บัตร
		- บันทึกเวลาเข้า
		- ส่งไปหา [1]
		- บันทึกลงใน csv เครื่องตัวเอง
'''