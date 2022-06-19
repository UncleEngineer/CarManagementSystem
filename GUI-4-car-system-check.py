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
serverip = '192.168.0.100' # IP of GUI-3-car-system-location.py
port = 9500
buffsize = 4096



GUI = Tk()
GUI.title('[4] Check')
GUI.geometry('500x500')

FONT = ('Angsana New',20)

L = Label(GUI,text='ป้ายทะเบียน',font=FONT)
L.pack()
v_plate = StringVar()
E1 = ttk.Entry(GUI,textvariable=v_plate,font=FONT)
E1.pack()

def CarCheck():
	plate = v_plate.get()
	text = 'check|'
	
	text += plate

	# Connect and Send
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	server.send(text.encode('utf-8'))
	data_server = server.recv(buffsize).decode('utf-8')
	print('Data from server: ', data_server)
	# location|3e30d2c4|in|toyota|red|A99|1001|2022-06-19 17:19:03|2F1|
	data_list = data_server.split('|')
	print('Your car zone: ',data_list[-2])
	server.close()
	print('--------------')

	text = 'รถยี่ห้อ: {}\nป้ายทะเบียน: {}\nจอดอยู่โซน: {}'.format(data_list[3],data_list[5],data_list[-2])
	v_result.set(text)


B1 = ttk.Button(GUI,text='ตรวจสอบ',command=CarCheck)
B1.pack(ipadx=30,ipady=20,pady=10)

v_result = StringVar()
v_result.set('---------Result--------')
R1 = Label(GUI,textvariable=v_result,font=(30))
R1.pack()



GUI.mainloop()