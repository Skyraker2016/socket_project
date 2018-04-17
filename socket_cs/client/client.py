# 客户端
import socket
import hashlib
import sys


def main():
    # 链接服务端ip和端口
    ip_port = ('127.0.0.1', 16337)
    # 生成一个socket对象
    sk = socket.socket()
    # 请求连接服务端
    sk.connect(ip_port)
    print("已连接到服务器")
    while 1:
        request = input("What do you want: ").strip()
        # 发送请求
        sk.send(request.encode())
        if (request == "quit"):
            break
        # 接受回应
        response = sk.recv(1024).decode()
        print(response)

        if (response == "wrong request!"):
            continue
        elif (response == "no such file!"):
            continue
        elif (response.split()[0] == "list"):
            print(response)
            continue
        elif (response.split()[1] == "filesize"):
            # 确认下载文件
            filesize = int(response.split()[2])
            tmp = filesize
            sure_request = input("Do you sure to download it?(y/n)").lower()
            sk.send(sure_request.encode())
            filename = response.split()[0]

            if (sure_request == 'y'):
                # 传输文件
                f = open(filename, 'wb')
                while (filesize > 0):
                    data = sk.recv(1024)
                    f.write(data)
                    filesize -= len(data)
                    progress = (tmp - filesize) / tmp
                    sys.stdout.write("Download progress: %d%%   \r" % (progress))
                    sys.stdout.flush()
                f.close()
                print("finish to download " + filename)
            else:
                continue
        else:
            continue

    sk.close()

if __name__ == "__main__":
    main()