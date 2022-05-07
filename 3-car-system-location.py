import socket
from datetime import datetime
############CSV##############
import csv
def writetocsv(data):
	# data = ['toyota','red','1A11','1001','2022-05-07 15:29:15']
	with open('2-car-system-in.csv','a',newline='',encoding='utf-8') as file:
		fw = csv.writer(file)
		fw.writerow(data) # no s is single line append
	print('csv saved')
############ADRESS##############
serverip = '192.168.0.100'

port = 9000
buffsize = 4096

while True:
	q = input('[1] - get multiple car information\n[2] - get single car information\n[q] - exit\n>>> ')
	if q == '1':
		text = 'location|allcar'
	elif q == '2':
		getcar = 'Enter Plate Code: '
		text = 'location|{}'.format(getcar)
	elif q == 'q':
		break
	
	# Connect and Send
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	server.send(text.encode('utf-8'))
	data_server = server.recv(buffsize).decode('utf-8')
	print('Data from server: ', data_server)
	server.close()



'''
[3]-car-system-location.py
	- client-1.py
	(function)
		- ดึงข้อมูลรถ ยี่ห้อ สี ป้ายทะเบียน บัตร จาก [1]
	- server.py
		- บันทึกตำแหน่งโซนของรถได้
		- ส่งข้อมูลรถไปยัง [4]
'''