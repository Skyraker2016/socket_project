# 客户端
import socket
import hashlib
import os
import math
import threading
import sys

def main():
    # 链接服务端ip和端口
    ip_port = ('127.0.0.1', 16330)
    my_port = ('127.0.0.1', 23330)

    while 1:  
        # 生成一个socket对象
        sk = socket.socket()
        # 请求连接服务端
        sk.bind(my_port)  
        sk.connect(ip_port)    
        print("已连接到服务器")
        request = input("What do you want: ").strip()

        if request.startswith("INIT"):
            fileNameList = os.listdir()
            initList = {}
            for filename in fileNameList:
                initList[filename] = os.stat(filename).st_size
            sk.send(("INIT "+str(initList)).encode())
            response = sk.recv(1024).decode()
            print(response)
        # 请求文件
        elif request.startswith("GET"):
            sk.send(request.encode())
            response = sk.recv(1024).decode()
            print(response)

        # 添加文件
        # TODO

        # 下线
        elif request.startswith("QUIT"):
            sk.send(request.encode())
            response = sk.recv(1024).decode()
            print(response)
            sk.close()
            break
        else:
            print("WRONG DOING")

        sk.close()

if __name__ == "__main__":
    main()