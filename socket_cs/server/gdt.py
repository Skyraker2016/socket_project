from tkinter import *
import time

class gdt():
    def __init__(self, name):
        self.name = name
        self.root = Tk()
        self.root.title(name)
        self.root.geometry('{}x{}'.format(250, 40))
        # 创建画布
        self.frame = Frame(self.root).grid(row=0, column=0)  # 使用时将框架根据情况选择新的位置
        self.canvas = Canvas(self.frame, width=205, height=30, bg="white")
        self.canvas.grid(row=0, column=0)
        self.x = StringVar()
        # 进度条以及完成程度
        self.out_rec = self.canvas.create_rectangle(5, 5, 200, 25, outline="blue", width=1)
        self.fill_rec = self.canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")

        Label(self.frame, textvariable=self.x).grid(row=0, column=1)

    # 更新进度条函数
    def change_schedule(self, now_schedule, all_schedule):
        self.canvas.coords(self.fill_rec, (5, 5, 6 + (now_schedule / all_schedule) * 195, 25))
        self.root.update()
        self.x.set(str(round(now_schedule / all_schedule * 100, 2)) + '%')
        if round(now_schedule / all_schedule * 100, 2) == 100.00:
            self.x.set("完成")


g = gdt("我是进度条呀")
for i in range(1,500):
    g.change_schedule(i, 500)
    time.sleep(0.01)
