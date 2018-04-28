from tkinter import *
import time

class gdt():
    def __init__(self, name, root, r):
        # 创建画布
        self.frame = Frame(root).grid(row=r, column=0)  # 使用时将框架根据情况选择新的位置
        self.canvas = Canvas(self.frame, width=205, height=30, bg="white")
        self.canvas.grid(row=r, column=2)
        self.x = StringVar()
        self.y = StringVar()
        # 进度条以及完成程度
        self.out_rec = self.canvas.create_rectangle(5, 5, 200, 25, outline="blue", width=1)
        self.fill_rec = self.canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")
        self.x.set("0.00%")
        self.y.set(name)
        Label(self.frame, textvariable=self.x, height=1, width=10).grid(row=r, column=1)
        Label(self.frame, textvariable=self.y, height=1, width=30).grid(row=r, column=0)

    # 更新进度条函数
    def change_schedule(self, now_schedule, all_schedule):
        self.canvas.coords(self.fill_rec, (5, 5, 6 + (now_schedule / all_schedule) * 195, 25))
        self.x.set(str(round(now_schedule / all_schedule * 100, 2)) + '%')
        if round(now_schedule / all_schedule * 100, 2) == 100.00:
            self.x.set("完成")



# root = Tk()
# A = gdt("A", root, 0)
# root.update()
# A.change_schedule(80,80)
# bb=input()
# B = gdt(bb, root, 1)
# root.update()
# input()