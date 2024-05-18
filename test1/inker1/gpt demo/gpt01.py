import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# 获取当前脚本的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建一个用户数据库（简单版，使用字典存储）
users = {}

# 主应用类
class OrderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("点餐系统")
        self.geometry("600x400")
        self.username = None
        self.frames = {}
        self.create_frames()
        self.show_frame("RegisterFrame")

    def create_frames(self):
        self.frames["RegisterFrame"] = RegisterFrame(self)
        self.frames["LoginFrame"] = LoginFrame(self)
        self.frames["OrderFrame"] = OrderFrame(self)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def register_user(self, username, password):
        if username in users:
            messagebox.showerror("错误", "用户名已存在")
        else:
            users[username] = password
            messagebox.showinfo("成功", "注册成功")
            self.show_frame("LoginFrame")

    def login_user(self, username, password):
        if username in users and users[username] == password:
            self.username = username
            self.show_frame("OrderFrame")
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    def place_order(self, order_details):
        messagebox.showinfo("订单已提交", f"订单详情：\n{order_details}")
        self.show_payment_qr()

    def show_payment_qr(self):
        self.withdraw()  # 隐藏主窗口
        payment_window = tk.Toplevel(self)
        payment_window.title("微信支付")
        payment_window.geometry("300x300")

        img_path = os.path.join(current_dir, "wechat_qr.png")
        if not os.path.isfile(img_path):
            messagebox.showerror("错误", f"未找到图片文件: {img_path}")
            return

        img = Image.open(img_path)  # 请确保有一个名为 wechat_qr.png 的支付截图
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(payment_window, image=photo)
        label.image = photo
        label.pack()

        def on_close():
            self.deiconify()  # 重新显示主窗口
            payment_window.destroy()

        payment_window.protocol("WM_DELETE_WINDOW", on_close)

        # 等待5秒后显示取餐号
        payment_window.after(5000, lambda: self.show_pickup_number(payment_window))

    def show_pickup_number(self, payment_window):
        payment_window.destroy()
        self.deiconify()  # 重新显示主窗口
        pickup_window = tk.Toplevel(self)
        pickup_window.title("取餐号")
        pickup_window.geometry("300x200")
        pickup_number = random.randint(1000, 9999)
        tk.Label(pickup_window, text=f"您的取餐号是：{pickup_number}", font=("Arial", 20)).pack(pady=50)
        tk.Button(pickup_window, text="确定", command=pickup_window.destroy).pack(pady=10)

# 注册页面
class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        tk.Label(self, text="注册", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="用户名").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        tk.Label(self, text="密码").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self, text="注册", command=self.register).pack(pady=20)
        tk.Button(self, text="已有账号？登录", command=lambda: master.show_frame("LoginFrame")).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.master.register_user(username, password)

# 登录页面
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        tk.Label(self, text="登录", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="用户名").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        tk.Label(self, text="密码").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self, text="登录", command=self.login).pack(pady=20)
        tk.Button(self, text="没有账号？注册", command=lambda: master.show_frame("RegisterFrame")).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.master.login_user(username, password)

# 点餐页面
class OrderFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.order = {}
        tk.Label(self, text="点餐", font=("Arial", 16)).pack(pady=10)
        self.menu_items = [
            ("汉堡", 20, os.path.join(current_dir, "burger.jpg")), 
            ("薯条", 10, os.path.join(current_dir, "fries.jpg")), 
            ("可乐", 5, os.path.join(current_dir, "cola.jpg"))
        ]
        for item, price, img in self.menu_items:
            self.add_menu_item(item, price, img)
        tk.Button(self, text="下单", command=self.place_order).pack(pady=20)

    def add_menu_item(self, item, price, img_path):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        if not os.path.isfile(img_path):
            messagebox.showerror("错误", f"未找到图片文件: {img_path}")
            return

        image = Image.open(img_path)
        image = image.resize((50, 50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        img_label = tk.Label(frame, image=photo)
        img_label.image = photo
        img_label.pack(side=tk.LEFT, padx=10)
        label = tk.Label(frame, text=f"{item} - {price}元")
        label.pack(side=tk.LEFT, padx=10)
        if item == "汉堡":
            self.add_burger_options(frame, item)
        else:
            add_button = tk.Button(frame, text="+", command=lambda i=item: self.add_to_order(i))
            add_button.pack(side=tk.RIGHT)

    def add_burger_options(self, frame, item):
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        chk1 = tk.Checkbutton(frame, text="加起司", variable=var1)
        chk1.pack(side=tk.LEFT)
        chk2 = tk.Checkbutton(frame, text="加酸黄瓜", variable=var2)
        chk2.pack(side=tk.LEFT)
        add_button = tk.Button(frame, text="+", command=lambda: self.add_to_order(item, var1.get(), var2.get()))
        add_button.pack(side=tk.RIGHT)

    def add_to_order(self, item, cheese=0, pickle=0):
        spec = ""
        if item == "汉堡":
            if cheese:
                spec += "加起司 "
            if pickle:
                spec += "加酸黄瓜"
        if item in self.order:
            self.order[item].append(spec.strip())
        else:
            self.order[item] = [spec.strip()]
        messagebox.showinfo("已添加", f"{item} {spec} 已添加到订单")

    def place_order(self):
        if not self.order:
            messagebox.showwarning("订单空", "请先选择菜品")
            return
        order_details = "\n".join([f"{item} {' '.join(specs)}" for item, specs in self.order.items()])
        self.master.place_order(order_details)

# 运行应用
if __name__ == "__main__":
    app = OrderApp()
    app.mainloop()
