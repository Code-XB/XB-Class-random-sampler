import tkinter as tk
from tkinter import ttk, messagebox
import random

FONT = "微软雅黑"

root = tk.Tk()
root.title("随机抽取同学")
root.geometry("700x550")

# 状态变量
mode = 1 # 0

char_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F']
def get_random_color():
    return f"\
#{char_list[random.randint(1, 15)]}{char_list[random.randint(0, 15)]}{char_list[random.randint(1, 15)]}\
{char_list[random.randint(1, 15)]}{char_list[random.randint(1, 15)]}{char_list[random.randint(1, 15)]}"

# 学生列表
student_list = ["安梓萱", "崔晟睿", "罗敬尧", "王尹希", "肖奕晨", "方佑康", "邹梦琪", "詹瑷玮", "赵元祺",
                "周煜坤", "杨婉懿", "普逸然", "赵翊同", "卡皮巴拉", "侯幸佑", "秦紫馨", "王浩睿", "龚舜宜",
                "张程翔", "柏懿", "曾夕曈", "柴铃清", "高寅宸", "普钰博", "李梓嫣", "高婉悦", "代馨钰",
                "丁语恬", "江勃锡", "李松琞", "刘京伦", "刘苡歆", "鲁子洋", "马皓翊", "宋禹良", "汪蕾妍",
                "王家祺", "魏钰宸", "严玥涵", "杨洛一", "杨锐淇", "周宸绪", "李逸娴", "周弈凯(嘤嘤嘤😭)"
               ]

def new_student():
    student_label.config(text=student_list[random.randint(0, 43)], fg=get_random_color())
    
def set_mode():
    global mode
    # 翻转模式
    # mode = 1 - mode

    messagebox.showinfo("提示", "分组模式暂不支持!")

def objects():
    # 添加界面组件
    global mode_label, subject_label, student_label, new_student_button, set_mode_button

    mode_label = tk.Label(root, text="全班模式", font=(FONT, 10), fg="#FFDC2C")
    mode_label.pack(anchor="ne", padx=25, pady=10)

    subject_label = tk.Label(root, text="抽取四叶草🍀同学", font=(FONT, 25), fg="#136C1C")
    subject_label.pack(pady=(30, 0))

    student_label = tk.Label(root, text="点击下方按钮抽取", font=(FONT, 20))
    student_label.pack(pady=(40, 0))

    new_student_button = tk.Button(root, text="抽选一名随机同学", font=(FONT, 10), bg="#004CFF", fg="#66FFF5", command=new_student)
    new_student_button.pack(pady=(35, 0))

    set_mode_button = tk.Button(root, text="切换为分组抽取模式", font=(FONT, 10), bg="#CC9600", fg="#FFD089", command=set_mode)
    set_mode_button.pack(pady=(30, 0))

    author_label = tk.Label(root, text="版权所有，侵权不敢揪  2025 (c) 制作者：张程翔  不保留权利😄", font=(FONT, 10), fg="#9d9d9d")
    author_label.pack(side="bottom", anchor="sw", padx=6, pady=5)

def main():
    objects()
    root.mainloop()


if __name__ == "__main__":
    main()