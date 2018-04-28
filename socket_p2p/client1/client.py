import os
import socket
import threading
import hashlib
import string
import random
import sys
import struct
import gdt
from tkinter import *

host_ip = "127.0.0.1"

server_ip_port = ("127.0.0.1", 16337)
# client_ip_port = (host_ip, 12345)
# client_s_ip_port = [(host_ip, i+12346) for i in range(10)]
data_out_port = 12340
lock = threading.Lock()
exitflag = 1
files_size = {}
files_temp = {}

drawLock = threading.Lock()
gdtList = {}  # title: [status, now, all]
change = True


def key_gen():
	ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
	return ran_str


def INIT():
	main_s = socket.socket()
	# main_s.bind(client_ip_port)
	flag = 1
	i = 0
	while i < 3 and flag:
		try:
			main_s.connect(server_ip_port)
			print("Connect Success")
			filenames = os.listdir()
			files = {}
			for filename in filenames:
				files[filename] = os.stat(filename).st_size
			print(files)
			main_s.send(("INIT "+str(data_out_port)+" "+str(files)).encode())
			response = main_s.recv(1024).decode()
			print(response)
			flag = 0
			main_s.close()
		except:
			print("Connect Fail")
			i += 1
			if(i == 3):
				print("The server has no reaction,INIT fails")
				main_s.close()
				os._exit(0)


def get_file(filename):
	global change, drawLock, gdtList
	main_s = socket.socket()
	# main_s.bind(client_ip_port)
	main_s.connect(server_ip_port)
	print("Connect Success")
	request = "GET "+str(filename)
	main_s.send(request.encode())
	response = main_s.recv(1024).decode()
	
	print(response)
	peerlist = {}
	if response == "ERROR YOU_ALREADY_GOT_IT" or response == "ERROR FILE_NOT_FOUND":
		print(response)
		return
	else:
		filesize = int(response.split()[1])
		if (filesize==0):
			print("without any content")
			return
		drawLock.acquire()
		# print("HEY")
		gdtList["v "+filename] = [False, 0, 100]
		change = True
		drawLock.release()
		d_len = len(response.split()[0])+len(response.split()[1])+2
		response = response[d_len:]
		peerlist = eval(response)
	lock.acquire()
	files_size[filename] = []
	files_size[filename].append(filesize)
	files_size[filename].append(0)
	files_temp[filename] = [0 for i in range(len(peerlist))]
	lock.release()
	'''
	初始化文件缓冲区
	'''
	id = 0
	for addr, part in peerlist.items():
		t = threading.Thread(target=get_file_client, args=(filename, addr, part, id))
		id += 1
		t.daemon = True
		t.start()
	'''
	创建多线程接收文件
	'''
	while True:
		lock.acquire()
		if files_size[filename][0] > files_size[filename][1]:
			lock.release()
			continue
		else:
			lock.release()
			break

	'''
	等待所有接收线程结束
	'''
	with open(filename, "wb") as file:
		for temp in files_temp[filename]:
			sub_file = open(temp, "rb")
			sub_file_size = os.stat(temp).st_size
			while sub_file_size > 0:
				data = sub_file.read(720)
				file.write(data)
				sub_file_size -= 720
			sub_file.close()
	for temp in files_temp[filename]:
		# print(temp)
		os.remove(temp)
	files_temp.pop(filename)
	'''
	从每一个临时文件读取文件内容，
	'''
	main_s.close()
	add_file(filename, filesize)
	print("DOWNLOAD Success")
	return


def get_file_client(filename, addr, part, id):
	global change, gdtList
	client_s = socket.socket()
	client_s.connect(addr)
	print("Connect Success ", str(addr))
	client_s.send(("DOWNLOAD "+filename+" "+str(part)).encode())
	# print(part)
	file_temp_name = key_gen()+".bin"
	# print(file_temp_name, str(id))
	lock.acquire()
	files_temp[filename][id] = file_temp_name
	# print(files_temp[filename][id])
	lock.release()
	f = open(file_temp_name, "wb")
	while 1:
		packet = client_s.recv(726)
		# print(len(packet))
		flag, index, data_len = struct.unpack("!3H", packet[:6])
		packet = packet[6:data_len+6]
		data = struct.unpack("!%ds" % data_len, packet)
		data = data[0]
		f.write(data)
		if flag:
			break
		lock.acquire()
		files_size[filename][1] += data_len
		lock.release()
		progress = 100*files_size[filename][1]/files_size[filename][0]
		# sys.stdout.write("Download progress: %f%%   \r" % (progress))
		# sys.stdout.flush()
		drawLock.acquire()
		# print("HEY AGAIN")
		change = True
		gdtList["v "+filename][1] = progress
		drawLock.release()
	lock.acquire()
	files_size[filename][1] += data_len
	progress = 100*files_size[filename][1]/files_size[filename][0]
	# sys.stdout.write("Download progress: %f%%   \r" % (progress))
	# sys.stdout.flush()
	drawLock.acquire()
	# print("WTFFFFF")
	change = True
	gdtList["v "+filename][1] = progress
	drawLock.release()
	f.close()
	lock.release()
	client_s.close()


def send_file(coon, filename, part):
	file = open(filename, "rb")
	for i in range(part[0]):
		file.read(720)
	for i in range(part[0], part[1]):
		data = file.read(720)
		if i < part[1]-1:
			pack = struct.pack("!3H%ds" % len(data), 0, i, len(data), data)
		else:
			pack = struct.pack("!3H%ds" % len(data), 1, i, len(data), data)
		coon.send(pack)
	# print("My work is done")
	file.close()
	return


def add_file(filename, filesize):
	main_s = socket.socket()
	# main_s.bind(client_ip_port)
	main_s.connect(server_ip_port)
	main_s.send(("ADD "+str(data_out_port)+" "+filename+" "+str(filesize)).encode())
	response = main_s.recv(1024).decode()
	print(response)


def Quit():
	lock.acquire()
	global exitflag
	main_s = socket.socket()
	# main_s.bind(client_ip_port)
	main_s.connect(server_ip_port)
	main_s.send(("QUIT"+" "+str(data_out_port)).encode())
	exitflag = 0
	main_s.close()
	print("I am going to die")
	lock.release()
	os._exit(0)
	return


def Client_main():
	# print("Cm")
	INIT()
	# print("heiheihei")
	while 1:
		command = input("Please input the command:")
		command = command.split()
		if command[0] == "GET":
			t = threading.Thread(target=get_file, args=(command[1],))
			t.daemon = True
			t.start()
		elif command[0] == "ADD":
			if(os.path.isfile(command[1])):
				add_file(command[1], os.stat(command[1]).st_size)
			else:
				print("You do not have such a file")
		elif command[0] == "QUIT":
			Quit()
			break
		else:
			print("Wrong command")
	return


def Serve_main(coon, addr):
	# print("Servermain")
	request = coon.recv(1024).decode()
	if request.split()[0] != "DOWNLOAD":
		coon.send(("ERROR").encode())
		return
	filename = request.split()[1]
	part_len = len(request.split()[0])+len(request.split()[1])+2
	request = request[part_len:]
	part = eval(request)
	send_file(coon, filename, part)


def Listen_main():
	# print("Listening")
	s = socket.socket()
	s.bind((host_ip, data_out_port))
	s.listen(5)
	while True:
			coon, addr = s.accept()
			t = threading.Thread(target=Serve_main, args=(coon, addr))
			t.daemon = True
			t.start()


def true_main():
	global exitflag
	# print("a")
	cm = threading.Thread(target=Client_main, args=())
	# cm.daemon = True
	cm.start()
	# print("b")
	lm = threading.Thread(target=Listen_main, args=())
	# lm.daemon = True
	lm.start()
	if exitflag == 0:
		os._exit(0)


def main():
	global change, exitflag, gdtList
	t = threading.Thread(target=true_main, args=())
	t.daemon = True
	t.start()
	gdtObj = {}
	root = Tk()
	root.title("Client")
	num = 0
	while True:
		if exitflag==0:
			break
		if change == False:
			continue
		else:
			# print("???")
			change = False
			drawLock.acquire()
		try:
			for title in gdtList.keys():
				# print(title+"!!!")
				l = gdtList[title]
				if l[0]:
					gdtObj[title].change_schedule(l[1], l[2])
				else:
					l[0] = True
					g = gdt.gdt(title, root, num)
					gdtObj[title] = g
					num += 1
		finally:
			drawLock.release()
		root.update()


if __name__=="__main__":
	main()
