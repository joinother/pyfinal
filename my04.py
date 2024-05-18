from tkinter import *
from tkinter import messagebox

class Application(Frame):
    """一个经典的GUI程序的类的写法"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createwidget()

    def createwidget(self):
        """创建组件"""
        self.btn01 = Button(self, text="登录", command=self.login)
        self.btn01.pack()

        # 加载图片
        self.image = PhotoImage(file=r"C:\Users\11348\Documents\py大作业\image.png")  # 替换为你的图片路径
        # 创建带有图片的按钮
        self.btn02 = Button(self, image=self.image, text="212", compound="left", command=self.login)
        self.btn02.pack()

    def login(self):
        messagebox.showinfo("成功")

if __name__ == '__main__':
    root = Tk()
    root.geometry("400x200+200+300")
    root.title("一个button测试")
    app = Application(master=root)
    root.mainloop()
