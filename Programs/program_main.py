import tkinter as tk
import random
import os
import threading

FONT = "微软雅黑"

def get_random_color():
    """生成更鲜艳的随机颜色"""
    bright_colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#FF9FF3', '#54A0FF',
        '#5F27CD', '#00D2D3', '#FF9F43', '#10AC84', '#EE5A24',
        '#A3CB38', '#1289A7', '#D980FA', '#B53471', '#FFC312'
    ]
    return random.choice(bright_colors)

root = tk.Tk()
root.geometry("700x550")
root.title("应用商城")
# root.iconbitmap("C:\\Users\\ASUS\\Desktop\\随机抽取同学\\images\\icon.ico")

subject_label = tk.Label(root, text="应用商店", font=(FONT, 25), fg=get_random_color())
subject_label.pack(pady=(20, 0))

time_button = tk.Button(root, text="计时器", font=(FONT, 10), command=lambda : start_porgram("计时器"), bg=get_random_color(), fg=get_random_color())
time_button.place(x=20, y=100)

tips_label = tk.Label(root, text="其他应用功能敬请期待", font=(FONT, 11), fg="#9d9d9d")
tips_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

prog_list = {
    "计时器" : "time.exe"
}

def start_porgram(name):
    def f():
        os.system(prog_list[name])
    thread = threading.Thread(target=f)
    thread.start()

def main():
    root.mainloop()
if __name__ == "__main__":
    main()