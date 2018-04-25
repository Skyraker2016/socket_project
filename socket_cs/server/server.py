# 服务端程序
import socket
import os
from threading import Thread
import gdt

def echo_client(conn, addr):
    print("已连接至 ",str(addr))
    # 获取客户端请求数据
    while 1:
        request = conn.recv(1024).decode()
        print(str(addr)+" request: "+request)
        if request.startswith("get"):
            if (len(request.split())!=2):
                conn.send("wrong request!".encode())
                continue
            else:
                filename = request.split()[1]
                if (os.path.isfile(filename)):
                    f = open(filename, 'rb')
                    filesize = os.stat(filename).st_size
                    conn.send((filename+" filesize "+str(filesize)).encode())
                    sure = conn.recv(1024).decode()
                    if sure=="y":
                        print("Uploading "+filename)
                        for data in f:
                            conn.send(data)
                        f.close()
                        print("finish uploading")
                    else:
                        continue
                else:
                    conn.send("no such file!".encode())
        elif request == "list":
            conn.send(("list "+str(os.listdir())).encode())
            continue
        elif request == "quit":
            print("bye bye" + str(addr))
            conn.close()
            break
        else:
            conn.send("wrong request!".encode())


def main():
    # 开启ip和端口
    ip_port = ('192.168.199.', 16337)
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
        t = Thread(target=echo_client, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    main()