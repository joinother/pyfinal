"""测试一个经典的Label组件写法,使用面向对象的方式"""
from tkinter import messagebox
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk 

class Application(Frame):     #继承了Frame
    """一个经典的GUI程序的类的写法"""
    
    def __init__(self,master=None):
        super().__init__(master)        #   super代表父类定义而不是对象
        self.master = master
        self.pack()


        self.createwidget()

    def createwidget(self):
        """创建组件"""
        self.label01 = Label(self,text="久久为功", width=10,height=2,
                             bg="black", fg="white")
        self.label01.pack()

        self.label02 = Label(self,text="百战百胜", width=10,height=2,
                            bg="blue", fg="white",font=("黑体", 30))
        self.label02.pack()

        # 添加图像
        self.image_path = r"C:\Users\11348\Documents\py大作业\image.png"  # 替换为你的图像路径
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_image = Label(self, image=self.photo)
        self.label_image.pack()


        #多行文本
        self.label04 = Label(self, text="有钱付首付\n没钱买别墅\n可以做糕点", 
                             borderwidth=4,relief="solid",justify="right")
        self.label04.pack()





if __name__ == '__main__':
    root = Tk()
    root.geometry("400x500+200+300")
    root.title("一个经典的GUI程序测试")
    app = Application(master=root)

    root.mainloop()

    