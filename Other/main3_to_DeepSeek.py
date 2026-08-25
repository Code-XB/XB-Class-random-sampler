import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import winsound

FONT = "微软雅黑"

root = tk.Tk()
root.title("随机抽取同学")
root.geometry("800x620")

# 状态变量
mode = 0  # 0:全班模式, 1:分组模式, 2:选择同学模式
selected_students_list = []
selected_groups = []

# 改进的颜色生成函数
def get_random_color():
    hues = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
    return random.choice(hues)

# 学生列表
student_list_group = [
    ["安梓萱", "崔晟睿", "罗敬尧"  , "王尹希", "肖奕晨", "方佑康", "邹梦琪"         ],
    ["刘苡歆", "柏懿"  , "柴铃清"  , "李松琞", "代馨钰", "马皓翊", "鲁子洋"         ],
    ["宋禹良", "李梓嫣", "邹梦琪"  , "高寅宸", "曾夕曈", "汪蕾妍", "周宸绪"         ],
    ["普钰博", "杨洛一", "王家祺"  , "魏钰宸", "丁语恬", "詹瑷玮", "赵元祺"         ],
    ["周煜坤", "杨婉懿", "杨锐淇"  , "江勃锡", "刘京伦", "李逸娴", "高婉悦"         ],
    ["普逸然", "赵翊同", "卡皮巴拉", "侯幸佑", "秦紫馨", "王浩睿", "龚舜宜", "张程翔"]
]

def get_now_group(original_group):
    """获取当前周的小组位置"""
    weeks_passed = int(time.time() // 604800)
    return (original_group - 1 + weeks_passed) % 6 + 1 + 2

def get_random_student():
    """根据模式获取随机学生"""
    if mode == 0:  # 全班模式
        group = random.randint(0, 5)
        if group < 5:
            return student_list_group[group][random.randint(0, 6)]
        else:
            return student_list_group[5][random.randint(0, 7)]
    
    elif mode == 1:  # 分组模式
        if not selected_groups:
            messagebox.showinfo("提示", "请先选择要抽取的组！")
            return None
        group_index = random.choice(selected_groups) - 1
        if group_index < 5:
            return student_list_group[group_index][random.randint(0, 6)]
        else:
            return student_list_group[5][random.randint(0, 7)]
    
    else:  # 选择同学模式
        if not selected_students_list:
            messagebox.showinfo("提示", "请先选择要抽取的同学！")
            return None
        return random.choice(selected_students_list)

def new_student():
    """抽取新学生"""
    # 添加抽取动画效果
    student_label.config(font=(FONT, 20), fg="#333333")
    
    for i in range(8):
        temp_student = get_random_student()
        if temp_student is None:
            return
        student_label.config(text=temp_student, fg=get_random_color())
        root.update()
        time.sleep(0.1)
    
    # 最终结果
    final_student = get_random_student()
    if final_student:
        student_label.config(text=final_student, fg="#FF0000", font=(FONT, 22, "bold"))
        # 显示恭喜信息
        messagebox.showinfo("抽取结果", f"抽取到 {final_student} 同学")

def group_select_window():
    """选择分组的窗口"""
    group_window = tk.Toplevel(root)
    group_window.title("选择分组")
    group_window.geometry("600x400")
    group_window.transient(root)
    group_window.grab_set()
    
    # 存储选择状态的字典
    selected_groups_vars = {}
    
    # 创建主框架
    main_frame = ttk.Frame(group_window)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # 创建标题
    title_label = tk.Label(main_frame, text="请选择要抽取的组", font=(FONT, 16, "bold"))
    title_label.pack(pady=10)
    
    # 说明文字
    info_label = tk.Label(main_frame, text="可以多选，将从选中的组中随机抽取", 
                         font=(FONT, 10), fg="#666666")
    info_label.pack(pady=(0, 20))
    
    # 创建分组选择框架
    group_frame = tk.Frame(main_frame)
    group_frame.pack(pady=10)
    
    # 创建6个分组的复选框
    for i in range(6):
        var = tk.BooleanVar()
        selected_groups_vars[i+1] = var
        
        cb = tk.Checkbutton(group_frame, text=f"第{i+1}组", variable=var,
                           font=(FONT, 12), bg='#F0F8FF')
        cb.grid(row=i//3, column=i%3, sticky='w', padx=20, pady=10, ipadx=5, ipady=2)
    
    # 控制按钮框架
    control_frame = tk.Frame(main_frame)
    control_frame.pack(pady=10)
    
    def select_all_groups():
        for var in selected_groups_vars.values():
            var.set(True)
    
    def select_no_groups():
        for var in selected_groups_vars.values():
            var.set(False)
    
    tk.Button(control_frame, text="全选", command=select_all_groups,
              bg="#4CAF50", fg="white", font=(FONT, 10)).pack(side='left', padx=10)
    tk.Button(control_frame, text="全不选", command=select_no_groups,
              bg="#F44336", fg="white", font=(FONT, 10)).pack(side='left', padx=10)
    
    # 底部按钮框架
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill='x', pady=20)
    
    result = []
    
    def confirm_selection():
        nonlocal result
        result = [group for group, var in selected_groups_vars.items() if var.get()]
        if not result:
            messagebox.showwarning("警告", "请至少选择一个组！")
            return
        group_window.destroy()
    
    def cancel_selection():
        nonlocal result
        result = []
        group_window.destroy()
    
    tk.Button(button_frame, text="确定", command=confirm_selection,
              bg="#2196F3", fg="white", font=(FONT, 12), width=10).pack(side='right', padx=10)
    tk.Button(button_frame, text="取消", command=cancel_selection,
              bg="#9E9E9E", fg="white", font=(FONT, 12), width=10).pack(side='right', padx=10)
    
    # 显示选择组数标签
    count_label = tk.Label(button_frame, text="已选择: 0 个组", font=(FONT, 12))
    count_label.pack(side='left', padx=10)
    
    def update_count():
        count = sum(1 for var in selected_groups_vars.values() if var.get())
        count_label.config(text=f"已选择: {count} 个组")
        group_window.after(100, update_count)
    
    update_count()
    
    group_window.wait_window(group_window)
    return result

def student_select_window():
    """选择学生的窗口"""
    student_window = tk.Toplevel(root)
    student_window.title("选择同学")
    student_window.geometry("800x650")
    student_window.transient(root)
    student_window.grab_set()
    
    selected_students = {}
    
    # 创建主框架
    main_frame = ttk.Frame(student_window)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # 创建标题
    title_label = tk.Label(main_frame, text="请选择同学", font=(FONT, 16, "bold"))
    title_label.pack(pady=10)
    
    # 创建滚动框架
    canvas = tk.Canvas(main_frame, bg='white')
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 创建复选框
    row_counter = 0
    for group_idx, group in enumerate(student_list_group):
        # 小组标题
        group_label = tk.Label(scrollable_frame, text=f"第{group_idx + 1}组:", 
                              font=(FONT, 12, "bold"), fg=get_random_color())
        group_label.grid(row=row_counter, column=0, columnspan=4, sticky='w', pady=(15, 5), padx=10)
        row_counter += 1
        
        # 学生复选框
        for i, student in enumerate(group):
            col = i % 4
            row = row_counter + (i // 4)
            
            var = tk.BooleanVar()
            selected_students[student] = var
            
            cb = tk.Checkbutton(scrollable_frame, text=student, variable=var,
                               font=(FONT, 11), bg='#F0F8FF')
            cb.grid(row=row, column=col, sticky='w', padx=15, pady=3)
        
        row_counter += (len(group) + 3) // 4
    
    # 控制按钮
    control_frame = tk.Frame(scrollable_frame, bg='white')
    control_frame.grid(row=row_counter, column=0, columnspan=4, pady=20)
    
    def select_all():
        for var in selected_students.values():
            var.set(True)
    
    def select_none():
        for var in selected_students.values():
            var.set(False)
    
    tk.Button(control_frame, text="全选", command=select_all, 
              bg="#4CAF50", fg="white", font=(FONT, 10)).pack(side='left', padx=10)
    tk.Button(control_frame, text="全不选", command=select_none,
              bg="#F44336", fg="white", font=(FONT, 10)).pack(side='left', padx=10)
    
    # 底部按钮
    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(fill='x', pady=10)
    
    result = []
    
    def confirm_selection():
        nonlocal result
        result = [student for student, var in selected_students.items() if var.get()]
        if not result:
            messagebox.showwarning("警告", "请至少选择一名同学！")
            return
        student_window.destroy()
    
    def cancel_selection():
        nonlocal result
        result = []
        student_window.destroy()
    
    tk.Button(button_frame, text="确定", command=confirm_selection,
              bg="#2196F3", fg="white", font=(FONT, 12), width=10).pack(side='right', padx=10)
    tk.Button(button_frame, text="取消", command=cancel_selection,
              bg="#9E9E9E", fg="white", font=(FONT, 12), width=10).pack(side='right', padx=10)
    
    # 计数标签
    count_label = tk.Label(button_frame, text="已选择: 0 人", font=(FONT, 12), bg='white')
    count_label.pack(side='left', padx=10)
    
    def update_count():
        count = sum(1 for var in selected_students.values() if var.get())
        count_label.config(text=f"已选择: {count} 人")
        student_window.after(100, update_count)
    
    update_count()
    
    # 布局
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    student_window.wait_window(student_window)
    return result

def set_mode(new_mode):
    """设置模式"""
    global mode, selected_students_list, selected_groups
    
    mode = new_mode
    
    # 更新模式显示
    mode_names = ["全班模式", "分组模式", "选择同学模式"]
    mode_label.config(text=mode_names[mode])
    
    # 更新按钮状态
    buttons = [all_class_button, group_button, select_students_button]
    for i, button in enumerate(buttons):
        if i == mode:
            button.config(bg="#FF5722", fg="white", font=(FONT, 12, "bold"))
        else:
            button.config(bg="#E0E0E0", fg="#333333", font=(FONT, 12))
    
    # 清空之前的选择
    if mode != 2:
        selected_students_list = []
    if mode != 1:
        selected_groups = []
    
    # 更新状态显示
    update_status_display()

def update_status_display():
    """更新状态显示"""
    if mode == 0:  # 全班模式
        status_label.config(text="状态: 将从全班同学中随机抽取")
    elif mode == 1:  # 分组模式
        if selected_groups:
            groups_text = "、".join([f"第{g}组" for g in selected_groups])
            status_label.config(text=f"状态: 将从{groups_text}中随机抽取")
        else:
            status_label.config(text="状态: 请选择要抽取的组")
    else:  # 选择同学模式
        if selected_students_list:
            if len(selected_students_list) <= 3:
                students_text = "、".join(selected_students_list)
                status_label.config(text=f"状态: 将从{students_text}中随机抽取")
            else:
                status_label.config(text=f"状态: 将从{len(selected_students_list)}名同学中随机抽取")
        else:
            status_label.config(text="状态: 请选择要抽取的同学")

def select_groups():
    """选择分组"""
    global selected_groups
    selected_groups = group_select_window()
    update_status_display()

def select_students():
    """选择学生"""
    global selected_students_list
    selected_students_list = student_select_window()
    update_status_display()

def objects():
    """创建界面组件"""
    global mode_label, subject_label, student_label, new_student_button
    global all_class_button, group_button, select_students_button, status_label, author_label
    
    # 设置窗口背景色
    root.configure(bg='#F5F5F5')
    
    # 模式显示
    mode_label = tk.Label(root, text="全班模式", font=(FONT, 14, "bold"), fg="#FF5722", bg='#F5F5F5')
    mode_label.pack(anchor="ne", padx=25, pady=(15, 10))
    
    # 主题
    subject_label = tk.Label(root, text="随机同学 🎉", font=(FONT, 27, "bold"), fg="#E91E63", bg='#F5F5F5')
    subject_label.pack(pady=(0, 30))
    
    # 学生显示
    student_label = tk.Label(root, text="点击下方按钮开始抽取", font=(FONT, 25), fg="#333333", bg='#F5F5F5')
    student_label.pack(pady=(20, 30))
    
    # 状态显示
    status_label = tk.Label(root, text="状态: 将从全班同学中随机抽取", 
                           font=(FONT, 11), fg="#666666", bg='#F5F5F5')
    status_label.pack(pady=(0, 20))
    
    # 主要抽取按钮
    new_student_button = tk.Button(root, text="开始抽取 🎯", font=(FONT, 16, "bold"), 
                                  bg="#FF5722", fg="white", height=2, width=20,
                                  command=new_student)
    new_student_button.pack(pady=(10, 30))
    
    # 模式选择按钮框架
    mode_frame = tk.Frame(root, bg='#F5F5F5')
    mode_frame.pack(pady=10)
    
    # 三个模式按钮
    all_class_button = tk.Button(mode_frame, text="全班模式", font=(FONT, 12, "bold"),
                                bg="#FF5722", fg="white", width=12, height=2,
                                command=lambda: set_mode(0))
    all_class_button.pack(side='left', padx=5)
    
    group_button = tk.Button(mode_frame, text="分组模式", font=(FONT, 12),
                            bg="#E0E0E0", fg="#333333", width=12, height=2,
                            command=lambda: set_mode(1))
    group_button.pack(side='left', padx=5)
    
    select_students_button = tk.Button(mode_frame, text="选择模式", font=(FONT, 12),
                                      bg="#E0E0E0", fg="#333333", width=12, height=2,
                                      command=lambda: set_mode(2))
    select_students_button.pack(side='left', padx=5)
    
    # 设置按钮框架
    setting_frame = tk.Frame(root, bg='#F5F5F5')
    setting_frame.pack(pady=15)
    
    # 分组设置按钮
    group_setting_button = tk.Button(setting_frame, text="选择分组", font=(FONT, 11),
                                    bg="#2196F3", fg="white", width=12,
                                    command=select_groups)
    group_setting_button.pack(side='left', padx=8)
    
    # 同学选择按钮
    student_setting_button = tk.Button(setting_frame, text="选择同学", font=(FONT, 11),
                                      bg="#2196F3", fg="white", width=12,
                                      command=select_students)
    student_setting_button.pack(side='left', padx=8)
    
    # 作者信息
    author_label = tk.Label(root, text="版权所有，侵权不敢揪  2025 (c) 制作者：张程翔  不保留权利😄", 
                           font=(FONT, 10), fg="#9d9d9d", bg='#F5F5F5')
    author_label.pack(side="bottom", anchor="sw", padx=10, pady=8)

def main():
    """主函数"""
    objects()
    # 初始化为全班模式
    set_mode(0)
    root.mainloop()

if __name__ == "__main__":
    main()