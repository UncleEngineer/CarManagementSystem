from tkinter import *
from tkinter import ttk, messagebox
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
    return (hour,minute,cal) # (hour,minute,fee)


############CSV##############
def writetocsv(data):
	# data = ['toyota','red','1A11','1001','2022-05-07 15:29:15']
	with open('2-car-system-in.csv','a',newline='',encoding='utf-8') as file:
		fw = csv.writer(file)
		fw.writerow(data) # no s is single line append
	print('csv saved')

############RUN SERVER##############
serverip = '192.168.0.100' # IP of GUI-1-car-system-out.py
port = 9000
buffsize = 4096

car_dict = {}
key_dict = {}

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
			plate = data.split('|')[3]
			print('PLATE:',plate)
			key_dict[plate] = key

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


GUI = Tk()
GUI.title('[1] Out')
GUI.geometry('500x500')
FONT = ('Angsana New',20)

L = Label(GUI,text='ป้ายทะเบียน',font=FONT)
L.pack()
v_plate = StringVar()
E1 = ttk.Entry(GUI,textvariable=v_plate,font=FONT)
E1.pack()

def CarOut():
	try:
		data_plate = v_plate.get()
		key = key_dict[data_plate]
		print('Result:',car_dict[key])
		result = car_dict[key]
		# ['db01f0f1', 'in', 'Toyota', 'red', 'A9999', '1001', '2022-06-19 17:09:07']
		hour, minute, fee = calculate_car_hour(result[-1])

		text = 'รถยนต์ป้ายทะเบียน: {}\nเวลาที่จอด: {} ชั่วโมง {} นาที\nค่าจอดรถ: {}บาท'.format(result[4],hour,minute,fee)
		v_result.set(text)
		del car_dict[key]
		del key_dict[data_plate]
	except:
		messagebox.showinfo('รถออกแล้ว','รถคันนี้ได้ออกไปแล้วหรือไม่มีข้อมูลในระบบ')

B1 = ttk.Button(GUI,text='รถออก',command=CarOut)
B1.pack(ipadx=30,ipady=20,pady=10)


v_result = StringVar()
v_result.set('---------Result--------')
R1 = Label(GUI,textvariable=v_result,font=(30))
R1.pack()


# Start Server
task = threading.Thread(target=OutServer)
task.start()

GUI.mainloop()