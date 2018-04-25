# 服务端程序
import socket
import os
import threading
import gdt
from tkinter import *

port = 20000
myIP = '127.0.0.1'
gdtList = {} # title: [status, now, all]
change = False
lock = threading.Lock()
drawLock = threading.Lock()

def upload(filename, conn, curport):
    global myIP, change, gdtList
    filesize = os.stat(filename).st_size
    conn.send(("FILE "+filename+" "+str(filesize)+" "+str((myIP, curport))).encode())
    data_socket = socket.socket()
    data_socket.bind((myIP, curport))
    data_socket.listen(5)
    cur_conn, client_addr = data_socket.accept()
    print(" Begin to UPLOADING "+filename)
    f = open(filename, 'rb')
    drawLock.acquire()
    try:
        gdtList[filename+str(client_addr)] = [False, 0, filesize]
        change = True
    finally:
        drawLock.release()
    tmp = 0
    for data in f:
        cur_conn.send(data)
        tmp += len(data)
        drawLock.acquire()
        try:
            change = True
            gdtList[filename+str(client_addr)][1] = tmp
            # print(filename+" "+str(tmp))
        finally:
            drawLock.release()

def echo_client(conn, addr):
    global port
    print("已连接至 ",str(addr))
    # 获取客户端请求数据
    while 1:
        request = conn.recv(1024).decode()
        print(str(addr)+" request: "+request)
        if (request.startswith("QUIT")):
            break
        elif (request.startswith("GET")):
            filename = request.lstrip("GET ")
            if os.path.isfile(filename):
                lock.acquire()
                try:
                    port += 1
                finally:
                    lock.release()
                t = threading.Thread(target=upload, args=(filename, conn, port))
                t.daemon = True
                t.start()
            else:
                conn.send("ERROR FILE_NOT_FOUND".encode())
        elif (request.startswith("LIST")):
            fileList = {}
            tmpList = os.listdir()
            for filename in tmpList:
                fileList[filename] = os.stat(filename).st_size
            conn.send(("LIST "+str(fileList)).encode())
        elif (request.startswith("UPLOAD")):
            print("ACCEPTING UPLOAD")
        else:
            print("SOMETHING WRONG")
    conn.close()  


def server_main():
    global myIP
    # 开启ip和端口
    ip_port = (myIP, 16330)
    # 生成一个socket对象
    sk = socket.socket()
    # 绑定ip端口
    sk.bind(ip_port)
    # 最多连接数
    sk.listen(5)
    # 开启死循环等待客户端连接
    print('服务器启动...')
    while True:
        # 等待链接,阻塞，直到渠道链接 conn打开一个新的对象专门给当前链接的客户端 addr是ip地址
        conn, addr = sk.accept()
        t = threading.Thread(target=echo_client, args=(conn, addr))
        t.daemon = True
        t.start()

def main():
    global change, gdtList
    t = threading.Thread(target=server_main, args=())
    t.daemon = True
    t.start()
    gdtObj = {}
    root = Tk()
    root.title("Server")
    num = 0
    while True:
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