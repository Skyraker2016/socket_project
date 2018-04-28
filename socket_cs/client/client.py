import socket
import hashlib
import sys
import gdt
import hashlib
import threading
from tkinter import *

myIP = '127.0.0.1'
gdtList = {} # title: [status, now, all]
change = False
lock = threading.Lock()
drawLock = threading.Lock()
quitFlag = False

def download(filename, filesize, server_port):
    global change, gdtList, drawLock
    print("Begin to download "+filename +" from "+str(server_port))
    dl_flag = 0
    dl = socket.socket()
    dl.connect(server_port)
    tmp = filesize
    while 1 - dl_flag:
        md5_c = hashlib.md5()
        filesize = tmp
        f = open(filename, 'wb')
        drawLock.acquire()
        try:
            gdtList[filename] = [False, 0, filesize]
            change = True
        finally:
            drawLock.release()
        while filesize>0:
            data = dl.recv(1024)
            md5_c.update(data)
            f.write(data)
            filesize -= len(data)
            drawLock.acquire()
            try:
                change = True
                gdtList[filename][1] = tmp-filesize
                # print(filename+" "+str(tmp))
            finally:
                drawLock.release()
        dl.send(str(md5_c.hexdigest()).encode())
        ackrecv = dl.recv(1024).decode()
        dl_flag = int(ackrecv)


def client_main():
    global quitFlag
    # 链接服务端ip和端口
    ip_port = (myIP, 16330)
    my_port = (myIP, 23330)
    # 生成一个socket对象
    sk = socket.socket()
    # sk.bind(my_port)
    # 请求连接服务端
    sk.connect(ip_port)
    print("已连接到服务器")
    while 1:
        request = input("What do you want: ").strip()
        # 发送请求
        sk.send(request.encode())
        if (request.startswith("QUIT")):
            sk.close()
            quitFlag = True
            break
        elif (request.startswith("GET")):
            response = sk.recv(1024).decode()
            if (response.startswith("ERROR")):
                print(response)
                continue
            else:
                filesize = int(response.split()[2])
                filename = request.lstrip("GET ").split()[0]
                response = response.lstrip("FILE ")
                response = response.lstrip(response.split()[0]+" ")
                response = response.lstrip(response.split()[0]+" ")# 去掉回应的filename、filesize
                server_port = eval(response)
                t = threading.Thread(target=download, args=(filename, filesize, server_port))
                t.daemon = True
                t.start()

        elif (request.startswith("LIST")):
            response = sk.recv(1024).decode()
            response = response.lstrip("LIST ")
            fileList = eval(response)
            print("------------------------")
            for key in fileList.keys():
                print(key + ": "+str(fileList[key]))
            print("------------------------")
        elif (request.startswith("UPLOAD")):
            print("UPLOADING")
        else:
            print("WRONG REQUEST, TRY AGAIN...")   


def main():
    global change, gdtList, drawLock
    t = threading.Thread(target=client_main, args=())
    t.daemon = True
    t.start()
    gdtObj = {}
    root = Tk()
    root.title("Client")
    num = 0
    while True:
        if quitFlag:
            break
        if change == False:
            continue
        else:
            change = False
        drawLock.acquire()
        try:
            for title in gdtList.keys():
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

if __name__ == "__main__":
    main()