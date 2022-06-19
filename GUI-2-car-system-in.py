from tkinter import *
from tkinter import ttk, messagebox
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
serverip = '192.168.0.100' # IP of GUI-1-car-system-out.py
port = 9000
buffsize = 4096

GUI = Tk()
GUI.title('[2] In')
GUI.geometry('500x500')
FONT = ('Angsana New',20)

L = Label(GUI,text='ยี่ห้อ',font=FONT)
L.pack()
v_brand = StringVar()
E1 = ttk.Entry(GUI,textvariable=v_brand,font=FONT)
E1.pack()

L = Label(GUI,text='สี',font=FONT)
L.pack()
v_color = StringVar()
E2 = ttk.Entry(GUI,textvariable=v_color,font=FONT)
E2.pack()

L = Label(GUI,text='ป้ายทะเบียน',font=FONT)
L.pack()
v_plate = StringVar()
E3 = ttk.Entry(GUI,textvariable=v_plate,font=FONT)
E3.pack()

L = Label(GUI,text='รหัสบัตรจอดรถ',font=FONT)
L.pack()

v_card = IntVar()
v_card.set(1001) #start card number
E4 = ttk.Entry(GUI,textvariable=v_card,font=FONT)
E4.pack()

def CarIn():

	info = {'brand':{'q':'Brand: ','value':''},
			'color':{'q':'Color: ','value':''},
			'plate':{'q':'Plate: ','value':''},
			'card':{'q':'Card: ','value':''}}
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	brand = v_brand.get()
	color = v_color.get()
	plate = v_plate.get()
	card = str(v_card.get())

	info['brand']['value'] = brand
	info['color']['value'] = color
	info['plate']['value'] = plate
	info['card']['value'] = card

	text = 'in|' # 'in|' is prefix from car-system-in
	print(info)

	for v in info.values():
		text += v['value'] + '|'

	text += timestamp

	print(text)

	writetocsv(text.split('|'))

	# Connect and Send
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	server.send(text.encode('utf-8'))
	data_server = server.recv(buffsize).decode('utf-8')
	print('Data from server: ', data_server)
	server.close()
	print('--------------')

	v_brand.set('')
	v_color.set('')
	v_plate.set('')
	newcard = v_card.get() + 1
	v_card.set(newcard)


B1 = ttk.Button(GUI,text='รถเข้า',command=CarIn)
B1.pack(ipadx=30,ipady=20,pady=10)


GUI.mainloop()