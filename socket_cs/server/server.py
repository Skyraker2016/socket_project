# 服务端程序
import socket
import os
import threading
import gdt
import hashlib
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

    drawLock.acquire()
    try:
        gdtList[filename+str(client_addr)] = [False, 0, filesize]
        change = True
    finally:
        drawLock.release()
    tmp = 0
    md5_flag = 0
    while 1 - md5_flag:
        md5_s = hashlib.md5()
        f = open(filename, 'rb')
        for data in f:
            md5_s.update(data)
            cur_conn.send(data)
            tmp += len(data)
            drawLock.acquire()
            try:
                change = True
                gdtList[filename+str(client_addr)][1] = tmp
            finally:
                drawLock.release()
        md5_c = cur_conn.recv(1024).decode()
        md5_s = str(md5_s.hexdigest())
        if md5_s == md5_c:
            md5_flag = 1
        cur_conn.send(str(md5_flag).encode())

def echo_client(conn, addr):
    global port
    wrong_time = 0
    print("已连接至 ",str(addr))
    # 获取客户端请求数据
    while 1:
        request = conn.recv(1024).decode()
        print(str(addr)+" request: "+request)
        if (request.startswith("QUIT")):
            wrong_time = 0
            break
        elif (request.startswith("GET")):
            wrong_time = 0
            filename = request.lstrip("GET ")
            if os.path.isfile(filename):
                lock.acquire()
                try:
                    port += 1
                    if port>=30000:
                        port = 20000
                finally:
                    lock.release()
                t = threading.Thread(target=upload, args=(filename, conn, port))
                t.daemon = True
                t.start()
            else:
                conn.send("ERROR FILE_NOT_FOUND".encode())
        elif (request.startswith("LIST")):
            wrong_time = 0
            fileList = {}
            tmpList = os.listdir()
            for filename in tmpList:
                fileList[filename] = os.stat(filename).st_size
            conn.send(("LIST "+str(fileList)).encode())
        elif (request.startswith("UPLOAD")):
            wrong_time = 0
            print("ACCEPTING UPLOAD")
        else:
            print("SOMETHING WRONG")
            wrong_time += 1
            if wrong_time >= 8:
                break
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