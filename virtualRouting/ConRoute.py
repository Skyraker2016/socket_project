import socket
import threading
import os

ip = 'aaa'
boss = ('127.0.0.1', 12306)
graph = {}
'''

DIJKSTRA
'''
def dijkstra():
    return
'''





'''
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def addPathGraph(x, y, val):
    global graph
    if x in graph:
            graph[x][y] = val
    else:
        graph[x] = {y: val}


def path(sip, dip, cost):
    addPathGraph(sip, dip, cost)
    addPathGraph(dip, sip, cost)
    killList = []
    for x in graph.keys():
        for y in graph[x].keys():
            if graph[x][y] >= 99999:
                killList.append((x, y))
    for death in killList:
        del graph[death[0]][death[1]]
    print(graph)
    

def ask(coon, dip): #TODO
    via = '8.8.8.8'
    dis = 99999
    coon.send(("ans "+via+" "+str(dis)).encode())

def allRoute(coon, sip):
    ar = {}
    coon.send(("all "+str(ar)).encode())


def listenMain():
    s = socket.socket()
    print(boss)
    s.bind(boss)
    s.listen(5)
    while True:
        coon, addr = s.accept()
        request = coon.recv(1024).decode()
        print(str(addr)+" REQUEST: "+request)
        if request.startswith("path "):
            dip = request.lstrip("path ").split()[0]
            dis = request.lstrip("path ").split()[1]
            path(addr[0], dip, int(dis))
        elif request.startswith("ask "):
            request = request.lstrip("ask ")
            ask(coon, request)
        elif request == "all":
            allRoute(coon, addr[0])

        coon.close()


def main():
    global ip
    global boss
    ip = get_host_ip()
    ip = '127.0.0.1'
    print("I'm "+ip)
    boss = (ip, 12306)
    print(boss)
    listenMain()

if __name__ == "__main__":
    main()