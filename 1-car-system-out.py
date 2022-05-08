import socket
import csv
import uuid
import threading

##############FEE##################
from datetime import datetime

def calculate_car_hour(dt='2022-05-08 12:27:18',first_hour=20,next_hour=10):
    # only hour and minute
    convert = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    delta = now - convert
    hour = delta.seconds // 3600
    minute = (delta.seconds % 3600) // 60
    print('Parking time: {} Hours {} minutes'.format(hour,minute))
    total = []
    if hour > 1:
        # ชั่วโมงแรก
        total.append(first_hour) # ชั่วโมงแรก 20
        total.append((hour - 1) * next_hour) # ชั่วโมงถัดไป
    elif hour == 1:
        total.append(first_hour)

    if minute > 15 and hour >= 1:
        total.append(next_hour)
    elif minute > 15 and hour == 0:
        total.append(first_hour)
    elif minute < 15:
        pass

    cal = sum(total)
    print('Car park fee: {} baht'.format(cal))

# calculate_car_hour('2022-05-08 8:27:18')
############CSV##############
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

car_dict = {}


def OutServer():
	while True:
		server = socket.socket()
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		server.bind((serverip,port))
		server.listen(1)
		print('waiting client...')

		client, addr = server.accept()
		print('connected from:', addr)

		data = client.recv(buffsize).decode('utf-8')
		print('Data from client: ',data)

		source = data.split('|')[0] # มาจากโปรแกรมฝั่งไหน? in / location / check

		if source == 'in':
			key = str(uuid.uuid1()).split('-')[0]
			car_dict[key] = data.split('|')
			# add key to value
			car_dict[key].insert(0,key)

			# - บันทึกข้อมูลที่ได้รับจาก [2]
			# write to csv
			writetocsv(data.split('|'))
			client.send('saved'.encode('utf-8'))
			client.close()
		elif source == 'location':
			text = 'out|'
			for k,v in car_dict.items():
				# text += k + '|' # ไม่ต้องส่งคีย์ไปเพราะมีการกรอกแล้ว
				for dt in v:
					text += dt + '|'

			print('Send to Location: ', text)
			client.send(text.encode('utf-8'))
			client.close()
		else:
			pass



task = threading.Thread(target=OutServer)
task.start()


while True:
	if len(car_dict) == 0:
		print('Not found car')
		q = input('Enter for continue..')
		print('-----')
	else:
		print()
		print('-------Select car out-------')
		car_number = {}
		car_plate = {}
		for i,c in enumerate(car_dict.items(),start=1):
			print('[{}]'.format(i) ,c)
			# Add key to c[1]
			# if len(c[1]) < 7:
			# 	c[1].insert(0,c[0])

			car_number[str(i)] = c[1] # only value
			car_plate[c[1][4]] = c[1]

		print('[P] - for enter plate no.')
		print('[R] - Refresh Data')
		print('------------')
		q = input('Select Car: ')

		if q == 'R' or q == '':
			continue



		# ['f583f7b5', 'in', 'toyota', 'red', '1A111', '1002', '2022-05-08 11:40:02']

		if q == 'P' or q == 'p':
			p = input('Enter Plate No. : ')
			print(car_plate[p])
			car = car_plate[p]
			calculate_car_hour(car[-1])
			del car_dict[car[0]] # clear data

		else:
			print(car_number[q])
			car = car_number[q]
			calculate_car_hour(car[-1])
			del car_dict[car[0]] # clear data

		print('------------')


















'''
[1]-car-system-out.py
	- server.py
	(function)
		- บันทึกเวลาออก
		- คำนวณชั่วโมงจอด
		- คำนวณค่าจอด
		- บันทึกข้อมูลที่ได้รับจาก [2]
'''