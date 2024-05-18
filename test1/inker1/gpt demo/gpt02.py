import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import random
import os

# 获取当前脚本的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建一个用户数据库（简单版，使用字典存储）
users = {}

# 生成推荐用户名
def generate_suggested_usernames(username):
    suggestions = [f"{username}{random.randint(100, 999)}" for _ in range(3)]
    return suggestions

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
        self.frames["PaymentFrame"] = PaymentFrame(self)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def register_user(self, username, password, security_question, security_answer):
        if username in users:
            suggestions = generate_suggested_usernames(username)
            messagebox.showerror("错误", f"用户名已存在，您可以尝试以下用户名：\n{', '.join(suggestions)}")
        else:
            users[username] = {"password": password, "security_question": security_question, "security_answer": security_answer}
            self.frames["LoginFrame"].update_username_menu()  # 更新用户名菜单
            messagebox.showinfo("成功", "注册成功")
            self.show_frame("LoginFrame")

    def login_user(self, username, password):
        if username in users and users[username]["password"] == password:
            self.username = username
            self.show_frame("OrderFrame")
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    def reset_password(self, username, security_answer, new_password):
        if username in users and users[username]["security_answer"] == security_answer:
            users[username]["password"] = new_password
            messagebox.showinfo("成功", "密码重置成功")
            self.show_frame("LoginFrame")
        else:
            messagebox.showerror("错误", "安全回答错误")

    def place_order(self, order_details, total_price):
        self.frames["PaymentFrame"].set_order_details(order_details, total_price)
        self.show_frame("PaymentFrame")

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
        tk.Label(self, text="安全问题").pack(pady=5)
        self.security_question_entry = tk.Entry(self)
        self.security_question_entry.pack(pady=5)
        tk.Label(self, text="安全问题答案").pack(pady=5)
        self.security_answer_entry = tk.Entry(self)
        self.security_answer_entry.pack(pady=5)
        tk.Button(self, text="注册", command=self.register).pack(pady=20)
        tk.Button(self, text="已有账号？登录", command=lambda: master.show_frame("LoginFrame")).pack(pady=5)
        tk.Button(self, text="返回", command=lambda: master.show_frame("LoginFrame")).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        security_question = self.security_question_entry.get()
        security_answer = self.security_answer_entry.get()
        self.master.register_user(username, password, security_question, security_answer)

# 登录页面
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        tk.Label(self, text="登录", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="用户名").pack(pady=5)
        self.username_entry = tk.StringVar()
        self.username_menu = tk.OptionMenu(self, self.username_entry, "")
        self.username_menu.pack(pady=5)
        tk.Label(self, text="密码").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self, text="登录", command=self.login).pack(pady=20)
        tk.Button(self, text="没有账号？注册", command=lambda: master.show_frame("RegisterFrame")).pack(pady=5)
        tk.Button(self, text="忘记密码", command=self.forgot_password).pack(pady=5)
        tk.Button(self, text="返回", command=lambda: master.show_frame("RegisterFrame")).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.master.login_user(username, password)

    def forgot_password(self):
        username = self.username_entry.get()
        if username not in users:
            messagebox.showerror("错误", "用户名不存在")
            return
        security_question = users[username]["security_question"]
        security_answer = simpledialog.askstring("安全问题", security_question)
        if security_answer:
            new_password = simpledialog.askstring("新密码", "请输入新密码", show="*")
            if new_password:
                self.master.reset_password(username, security_answer, new_password)

    def update_username_menu(self):
        menu = self.username_menu["menu"]
        menu.delete(0, "end")
        for username in users.keys():
            menu.add_command(label=username, command=lambda value=username: self.username_entry.set(value))

# 点餐页面
class OrderFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.order = {}
        self.total_price = 0
        self.discount_applied = False
        tk.Label(self, text="点餐", font=("Arial", 16)).pack(pady=10)
        self.menu_items = [
            ("汉堡", 20, os.path.join(current_dir, "burger.jpg")), 
            ("薯条", 10, os.path.join(current_dir, "fries.jpg")), 
            ("可乐", 5, os.path.join(current_dir, "cola.jpg"))
        ]
        for item, price, img in self.menu_items:
            self.add_menu_item(item, price, img)
        self.total_price_label = tk.Label(self, text="总价: 0元", font=("Arial", 14))
        self.total_price_label.pack(pady=10)
        tk.Button(self, text="下单", command=self.place_order).pack(pady=20)
        tk.Button(self, text="返回", command=lambda: master.show_frame("LoginFrame")).pack(pady=5)

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
            self.add_burger_options(frame, item, price)
        else:
            self.add_item_buttons(frame, item, price)

    def add_burger_options(self, frame, item, price):
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        chk1 = tk.Checkbutton(frame, text="加起司", variable=var1)
        chk1.pack(side=tk.LEFT)
        chk2 = tk.Checkbutton(frame, text="加酸黄瓜", variable=var2)
        chk2.pack(side=tk.LEFT)
        add_button = tk.Button(frame, text="+", command=lambda: self.add_to_order(item, price, var1.get(), var2.get()))
        add_button.pack(side=tk.RIGHT)

    def add_item_buttons(self, frame, item, price):
        add_button = tk.Button(frame, text="+", command=lambda: self.add_to_order(item, price))
        add_button.pack(side=tk.RIGHT)
        remove_button = tk.Button(frame, text="-", command=lambda: self.remove_from_order(item, price))
        remove_button.pack(side=tk.RIGHT)

    def add_to_order(self, item, price, cheese=0, pickle=0):
        spec = ""
        if item == "汉堡":
            if cheese:
                spec += "加起司 "
            if pickle:
                spec += "加酸黄瓜"
        if item in self.order:
            self.order[item].append((spec.strip(), price))
        else:
            self.order[item] = [(spec.strip(), price)]
        self.update_total_price(price)
        messagebox.showinfo("已添加", f"{item} {spec} 已添加到订单")
        self.check_discount()

    def remove_from_order(self, item, price):
        if item in self.order and self.order[item]:
            self.order[item].pop()
            self.update_total_price(-price)
            if not self.order[item]:
                del self.order[item]
            messagebox.showinfo("已移除", f"{item} 已从订单中移除")

    def update_total_price(self, price_change):
        self.total_price += price_change
        self.total_price_label.config(text=f"总价: {self.total_price}元")

    def check_discount(self):
        if all(item in self.order for item in ["汉堡", "薯条", "可乐"]) and not self.discount_applied:
            self.total_price *= 0.7
            self.total_price = round(self.total_price, 2)
            self.total_price_label.config(text=f"总价: {self.total_price}元")
            messagebox.showinfo("优惠", "三件商品已点齐，总价享受7折优惠！")
            self.discount_applied = True

    def place_order(self):
        if not self.order:
            messagebox.showwarning("订单空", "请先选择菜品")
            return
        order_details = "\n".join([f"{item} {' '.join(spec[0] for spec in specs)} ({len(specs)}份)" for item, specs in self.order.items()])
        self.master.place_order(order_details, self.total_price)

# 付款页面
class PaymentFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.order_details = ""
        self.total_price = 0
        tk.Label(self, text="微信支付", font=("Arial", 16)).pack(pady=10)
        self.qr_label = tk.Label(self)
        self.qr_label.pack(pady=10)
        self.countdown_label = tk.Label(self, text="", font=("Arial", 14))
        self.countdown_label.pack(pady=10)
        tk.Button(self, text="已付款？点我", command=self.show_pickup_number).pack(pady=10)
        tk.Button(self, text="返回", command=lambda: master.show_frame("OrderFrame")).pack(pady=5)

    def set_order_details(self, order_details, total_price):
        self.order_details = order_details
        self.total_price = total_price
        self.show_payment_qr()
        self.start_countdown(15)

    def show_payment_qr(self):
        img_path = os.path.join(current_dir, "wechat_qr.png")
        if not os.path.isfile(img_path):
            messagebox.showerror("错误", f"未找到图片文件: {img_path}")
            return

        img = Image.open(img_path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.qr_label.config(image=photo)
        self.qr_label.image = photo

    def start_countdown(self, seconds):
        self.remaining_time = seconds
        self.update_countdown()

    def update_countdown(self):
        if self.remaining_time > 0:
            self.countdown_label.config(text=f"{self.remaining_time}秒后返回点餐页面")
            self.remaining_time -= 1
            self.after(1000, self.update_countdown)
        else:
            self.master.show_frame("OrderFrame")
            messagebox.showwarning("未付款", "未付款，请重试")

    def show_pickup_number(self):
        pickup_window = tk.Toplevel(self)
        pickup_window.title("取餐号")
        pickup_window.geometry("300x200")
        pickup_number = random.randint(1000, 9999)
        tk.Label(pickup_window, text=f"您的取餐号是：{pickup_number}", font=("Arial", 20)).pack(pady=50)
        tk.Button(pickup_window, text="确定", command=pickup_window.destroy).pack(pady=10)

# 运行应用
if __name__ == "__main__":
    app = OrderApp()
    app.mainloop()
