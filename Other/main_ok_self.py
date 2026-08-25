import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

FONT = "微软雅黑"

root = tk.Tk()
root.title("随机抽取同学")
root.geometry("700x550")

inget_student_list = []
which_list = []

# 状态变量
mode = 0
whiching = False

char_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F']
def get_random_color():
    return f"\
#{char_list[random.randint(1, 15)]}{char_list[random.randint(0, 15)]}{char_list[random.randint(1, 15)]}\
{char_list[random.randint(1, 15)]}{char_list[random.randint(1, 15)]}{char_list[random.randint(1, 15)]}"

# 学生列表
student_list_group = [    # 分组
                ["安梓萱", "崔晟睿", "罗敬尧"  , "王尹希", "肖奕晨", "方佑康", "邹梦琪"],
                ["刘苡歆", "柏懿"  , "柴铃清"  , "李松琞", "代馨钰", "马皓翊", "鲁子洋"],
                ["宋禹良", "李梓嫣", "邹梦琪"  , "高寅宸", "曾夕曈", "汪蕾妍", "周宸绪"],
                ["普钰博", "杨洛一", "王家祺"  , "魏钰宸", "丁语恬", "詹瑷玮", "赵元祺"],
                ["周煜坤", "杨婉懿", "杨锐淇"  , "江勃锡", "刘京伦", "李逸娴", "高婉悦"],
                ["普逸然", "赵翊同", "卡皮巴拉", "侯幸佑", "秦紫馨", "王浩睿", "龚舜宜", "张程翔"]]

student_list_a = ["安梓萱", "崔晟睿", "罗敬尧", "王尹希", "肖奕晨"  , "方佑康", "邹梦琪", "詹瑷玮", "赵元祺",
                  "周煜坤", "杨婉懿", "普逸然", "赵翊同", "卡皮巴拉", "侯幸佑", "秦紫馨", "王浩睿", "龚舜宜",
                  "张程翔", "柏懿"  , "曾夕曈", "柴铃清", "高寅宸"  , "普钰博", "李梓嫣", "高婉悦", "代馨钰",
                  "丁语恬", "江勃锡", "李松琞", "刘京伦", "刘苡歆"  , "鲁子洋", "马皓翊", "宋禹良", "汪蕾妍",
                  "王家祺", "魏钰宸", "严玥涵", "杨洛一", "杨锐淇"  , "周宸绪", "李逸娴", "周弈凯(嘤嘤嘤😭)"]

def get_now_group(original_group):
    return int((original_group - 1 + int(time.time() // 604800)) % 6)

# 抽取同学函数
def new_student():
    global which_list
    def get_randomstudent_a():
        t = random.randint(0, 6)
        if t < 5: return student_list_group[t][random.randint(0, 6)]
        else: return student_list_group[5][random.randint(0, 7)]
    def get_randomstudent_t(t):
        if t < 5: return student_list_group[t][random.randint(0, 6)]
        else: return student_list_group[5][random.randint(0, 7)]
    
    if not which_list:
        which_list = which_window()
        if not which_list:
            which_list = [-1]
    else:
        if mode == 0:
            student_label.config(text=get_randomstudent_a(), fg=get_random_color())
        elif mode == 1:
            student_label.config(text=get_randomstudent_t(get_now_group(int(group_spinbox.get())-1)), fg=get_random_color())

def which_window():
    # 选择小组或某些同学
    which = tk.Tk()
    which.title("选取部分同学")
    which.geometry("800x650")
    
    # 存储选择状态的字典
    selected_students = {}
    
    # 创建主框架
    main_frame = ttk.Frame(which)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # 创建标题
    title_label = ttk.Label(main_frame, text="请选择同学（按小组显示）", font=(FONT, 16, "bold"))
    title_label.pack(pady=10)
    
    # 创建滚动框架
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 分组学生名单
    student_list_group = [
        ["安梓萱", "崔晟睿", "罗敬尧", "王尹希", "肖奕晨", "方佑康", "邹梦琪"],
        ["刘苡歆", "柏懿", "柴铃清", "李松琞", "代馨钰", "马皓翊", "鲁子洋"],
        ["宋禹良", "李梓嫣", "邹梦琪", "高寅宸", "曾夕曈", "汪蕾妍", "周宸绪"],
        ["普钰博", "杨洛一", "王家祺", "魏钰宸", "丁语恬", "詹瑷玮", "赵元祺"],
        ["周煜坤", "杨婉懿", "杨锐淇", "江勃锡", "刘京伦", "李逸娴", "高婉悦"],
        ["普逸然", "赵翊同", "卡皮巴拉", "侯幸佑", "秦紫馨", "王浩睿", "龚舜宜", "张程翔"]
    ]
    
    # 创建按小组显示的复选框
    row_counter = 0
    for group_idx, group in enumerate(student_list_group):
        # 小组标题
        group_label = ttk.Label(scrollable_frame, text=f"第{group_idx + 1}组:", font=(FONT, 18, "bold"), foreground=get_random_color())
        group_label.grid(row=row_counter, column=0, columnspan=4, sticky='w', pady=(10, 5), padx=10)
        row_counter += 1
        
        # 小组内学生复选框 - 使用 tk.Checkbutton 而不是 ttk.Checkbutton
        for i, student in enumerate(group):
            col = i % 4
            row = row_counter + (i // 4)
            
            # 创建变量来跟踪选择状态
            var = tk.BooleanVar()
            selected_students[student] = var
            
            # 创建复选框 - 使用 tk.Checkbutton
            cb = tk.Checkbutton(
                scrollable_frame, 
                text=student, 
                variable=var,
                font=(FONT, 13)  # 可以设置字体
            )
            cb.grid(row=row, column=col, sticky='w', padx=15, pady=2, ipadx=5, ipady=1)
        
        row_counter += (len(group) + 3) // 4  # 计算下一组的起始行
    
    # 全选/全不选框架
    select_all_frame = ttk.Frame(scrollable_frame)
    select_all_frame.grid(row=row_counter, column=0, columnspan=4, pady=20)
    
    def select_all():
        for var in selected_students.values():
            var.set(True)
    
    def select_none():
        for var in selected_students.values():
            var.set(False)
    
    # 使用 tk.Button 保持一致性
    tk.Button(select_all_frame, text="全选", command=select_all).pack(side='left', padx=10)
    tk.Button(select_all_frame, text="全不选", command=select_none).pack(side='left', padx=10)
    
    # 按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill='x', pady=10)
    
    # 存储结果的变量
    result = []
    
    def confirm_selection():
        nonlocal result
        result = [student for student, var in selected_students.items() if var.get()]
        which.destroy()
    
    def cancel_selection():
        nonlocal result
        result = []
        which.destroy()
    
    tk.Button(button_frame, text="确定", command=confirm_selection).pack(side='right', padx=10)
    tk.Button(button_frame, text="取消", command=cancel_selection).pack(side='right', padx=10)
    
    # 显示选择人数标签
    count_label = ttk.Label(button_frame, text="已选择: 0 人", font=(FONT, 15))
    count_label.pack(side='left', padx=10)
    
    def update_count():
        count = sum(1 for var in selected_students.values() if var.get())
        count_label.config(text=f"已选择: {count} 人")
        which.after(100, update_count)
    
    update_count()
    
    # 打包滚动区域
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # 等待窗口关闭
    which.wait_window(which)
    
    return result

def set_mode():
    global mode

    # 翻转模式
    mode = 1 - mode

    if mode == 0:
        set_mode_button.config(text="切换为部分抽取模式")
        mode_label.config(text="全班模式")
        group_spinbox.pack_forget()
        group_label.pack_forget()
        new_student_button.pack(pady=(35, 0))
    elif mode == 1:
        set_mode_button.config(text="切换为全班抽取模式")
        mode_label.config(text="部分模式")
        new_student_button.pack_forget()
        set_mode_button.pack_forget()
        group_spinbox.pack(pady=(20, 0), padx=(0, 300), side=tk.RIGHT)
        group_label.pack(pady=(20, 0), padx=(0, 0), side=tk.RIGHT)
        new_student_button.pack(pady=(20, 0))
        set_mode_button.pack(pady=(30, 0))

def set_students():
    global which_list
    if not which_list:
        which_list = which_window()

def objects():
    # 添加界面组件
    global mode_label, subject_label, student_label, new_student_button, set_mode_button, author_label, group_spinbox, group_label, which_student_button

    mode_label = tk.Label(root, text="全班模式", font=(FONT, 10), fg="#000000")
    mode_label.pack(anchor="ne", padx=25, pady=10)

    subject_label = tk.Label(root, text="抽取四叶草🍀同学", font=(FONT, 25), fg="#136C1C")
    subject_label.pack(pady=(30, 0))

    student_label = tk.Label(root, text="点击下方按钮抽取", font=(FONT, 20))
    student_label.pack(pady=(40, 0))

    group_label = tk.Label(root, text="输入组数：", font=(FONT, 10))
    group_spinbox = ttk.Spinbox(root, from_=1, to=7, wrap=True, increment=1, width=5)

    new_student_button = tk.Button(root, text="抽选一名随机同学", font=(FONT, 10), bg="#004CFF", fg="#66FFF5", command=new_student)
    new_student_button.pack(pady=(35, 0))

    set_mode_button = tk.Button(root, text="切换为部分抽取模式", font=(FONT, 10), bg="#CC9600", fg="#FFD089", command=set_mode)
    set_mode_button.pack(pady=(30, 0))

    which_student_button = tk.Button(root, text="选取部分同学", font=(FONT, 10), bg="#CC9600", fg="#FFD089", command=set_students)
    which_student_button.pack(pady=(30, 0))

    author_label = tk.Label(root, text="版权所有，侵权不敢揪  2025 (c) 制作者：张程翔  不保留权利😄", font=(FONT, 10), fg="#9d9d9d")
    author_label.pack(side="bottom", anchor="sw", padx=6, pady=5)

def main():
    objects()
    root.mainloop()

if __name__ == "__main__":
    main()