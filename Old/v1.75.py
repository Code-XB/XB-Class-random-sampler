import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

FONT = "微软雅黑"

root = tk.Tk()
root.title("随机抽取同学")
root.geometry("800x670")

# 状态变量
mode = 0  # 0:全班模式, 1:分组模式, 2:数量模式
selected_students_list = []
current_groups = []  # 改为列表，支持多个分组
build_num = "1.80.1"

def get_random_color():
    """生成更鲜艳的随机颜色"""
    bright_colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#FF9FF3', '#54A0FF',
        '#5F27CD', '#00D2D3', '#FF9F43', '#10AC84', '#EE5A24',
        '#A3CB38', '#1289A7', '#D980FA', '#B53471', '#FFC312'
    ]
    return random.choice(bright_colors)

# 学生列表
student_list_group = [
    ["安zai萱", "崔晟睿", "罗敬尧" , "王尹希", "小肖" , "方佑康", "邹梦琪"          ],
    ["刘苡歆", "柏懿"  , "柴铃清"  , "松果"  , "代馨钰", "马皓翊", "鲁子洋"         ],
    ["宋禹良", "李梓嫣", "邹梦琪"  , "高寅宸", "曾夕曈", "汪蕾妍", "周宸绪"         ],
    ["普钰博", "杨洛一", "王家祺"  , "魏钰宸", "丁语恬", "詹瑷玮", "赵元祺"         ],
    ["周煜坤", "杨婉懿", "杨锐淇"  , "江勃锡", "京宝"  , "李逸娴", "高婉悦"         ],
    ["普逸然", "赵翊同", "卡皮巴拉", "侯幸佑", "秦紫馨", "王浩睿", "龚舜宜", "张程翔"]
]

def tg_num(n):
    return int((time.time()//604800-2918+n)%6)

def get_random_student():
    if mode == 0:  # 全班模式
        group = random.randint(0, 5)
        if group < 5:
            return student_list_group[group][random.randint(0, 6)]
        else:
            return student_list_group[5][random.randint(0, 7)]
    elif mode == 1:  # 分组模式
        if selected_students_list:
            return random.choice(selected_students_list)
        else:
            # 从选中的多个分组中随机选择
            if current_groups:
                # 随机选择一个分组
                group_index = random.choice(current_groups) - 1
                if group_index < 5:
                    return student_list_group[group_index][random.randint(0, 6)]
                else:
                    return student_list_group[5][random.randint(0, 7)]
            else:
                # 如果没有选择分组，随机从全班选
                group = random.randint(0, 5)
                if group < 5:
                    return student_list_group[group][random.randint(0, 6)]
                else:
                    return student_list_group[5][random.randint(0, 7)]
    else:  # 数量模式
        group = random.randint(0, 5)
        if group < 5:
            return student_list_group[group][random.randint(0, 6)]
        else:
            return student_list_group[5][random.randint(0, 7)]

def get_multiple_students(count):
    """获取指定数量的随机学生（不重复）"""
    if mode == 1 and selected_students_list:  # 在分组模式下，从已选学生中抽取
        if count > len(selected_students_list):
            count = len(selected_students_list)
        return random.sample(selected_students_list, count)
    else:  # 其他模式从全班抽取
        all_students = []
        for group in student_list_group:
            all_students.extend(group)
        
        if count > len(all_students):
            count = len(all_students)
        
        return random.sample(all_students, count)

def new_student():
    global selected_students_list
    
    if mode == 1:  # 分组模式
        # 在分组模式下，如果没有选择具体学生也没有选择分组，才提示 "未选择" 消息
        if not selected_students_list and not current_groups:
            messagebox.showinfo("提示", "请先选择要抽取的同学或分组！")
            return
    
    global cleaned
    cleaned = False

    # 检查是否选择了抽取人数（针对选择同学模式）
    if mode == 1 and selected_students_list and hasattr(set_students, 'selected_count'):
        count = set_students.selected_count
        
        # 添加抽取动画效果
        student_label.config(font=(FONT, 20))  # 不加粗
        for i in range(random.randint(5, 15)):
            temp_student = get_random_student()
            student_label.config(text=temp_student, fg=get_random_color())
            root.update()
            time.sleep(0.1)
        
        students = random.sample(selected_students_list, min(count, len(selected_students_list)))
        
        if count == 1:
            final_student = students[0]
            student_label.config(text=final_student, fg="#FF0000", font=(FONT, 22, 'bold'))  # 加粗
            messagebox.showinfo("抽取结果", f"恭喜 {final_student} 同学！")
        else:
            students_text = "、".join(students)
            student_label.config(text=f"共抽取{count}名同学", fg="#FF0000", font=(FONT, 18, 'bold'))  # 加粗
            messagebox.showinfo("抽取结果", f"恭喜以下{count}名同学：\n\n{students_text}")
            student_label.config(text=students_text, wraplength=630, justify="center", font=(FONT, 22), fg="#FF0000")
        return
    
    # 如果是分组模式且选择了整个组（不是具体学生），并且设置了抽取人数
    if mode == 1 and not selected_students_list and current_groups and hasattr(group_select_window, 'selected_count'):
        count = group_select_window.selected_count
        
        # 合并所有选中分组的学生
        all_students = []
        for group_index in current_groups:
            group_idx = group_index - 1
            all_students.extend(student_list_group[group_idx])
        
        # 去重（如果有重复学生）
        all_students = list(set(all_students))
        
        if count > len(all_students):
            count = len(all_students)
        
        students = random.sample(all_students, count)
        
        # 添加抽取动画效果
        student_label.config(font=(FONT, 20))  # 不加粗
        for i in range(random.randint(5, 15)):
            temp_student = get_random_student()
            student_label.config(text=temp_student, fg=get_random_color())
            root.update()
            time.sleep(0.1)
        
        if count == 1:
            final_student = students[0]
            student_label.config(text=final_student, fg="#FF0000", font=(FONT, 22, 'bold'))  # 加粗
            messagebox.showinfo("抽取结果", f"恭喜 {final_student} 同学！")
        else:
            students_text = "、".join(students)
            student_label.config(text=f"共抽取{count}名同学", fg="#FF0000", font=(FONT, 18, 'bold'))  # 加粗
            messagebox.showinfo("抽取结果", f"恭喜以下{count}名同学：\n\n{students_text}")
            student_label.config(text=students_text, wraplength=630, justify="center", font=(FONT, 22), fg="#FF0000")
    else:
        # 原有逻辑（单个学生抽取）
        # 添加抽取动画效果
        student_label.config(font=(FONT, 20))  # 不加粗
        for i in range(random.randint(5, 15)):
            temp_student = get_random_student()
            student_label.config(text=temp_student, fg=get_random_color())
            root.update()
            time.sleep(0.1)
        
        final_student = get_random_student()
        student_label.config(text=final_student, fg="#FF0000", font=(FONT, 22, 'bold'))  # 加粗
        messagebox.showinfo("抽取结果", f"恭喜 {final_student} 同学！")

def new_multiple_students():
    """抽取多个学生"""
    if not hasattr(new_multiple_students, 'selected_count') or new_multiple_students.selected_count is None:
        messagebox.showinfo("提示", "请先设置抽取数量！")
        return
    
    count = new_multiple_students.selected_count
    students = get_multiple_students(count)

    student_label.config(font=(FONT, 20))  # 确保不加粗
    for i in range(random.randint(5, 15)):
        temp_student = get_random_student()
        student_label.config(text=temp_student, fg=get_random_color())
        root.update()
        time.sleep(0.1)
    
    # 显示结果
    if count == 1:
        student_label.config(text=students[0], fg="#FF0000", font=(FONT, 22, 'bold'))  # 加粗
        messagebox.showinfo("抽取结果", f"恭喜 {students[0]} 同学！")
    else:
        students_text = "、".join(students)
        student_label.config(text=f"共抽取{count}名同学", fg="#FF0000", font=(FONT, 18, 'bold'))  # 加粗
        messagebox.showinfo("抽取结果", f"恭喜以下{count}名同学：\n\n{students_text}")
        student_label.config(text=students_text, wraplength=630, justify="center", font=(FONT, 22), fg="#FF0000")

def which_window():
    which = tk.Toplevel(root)
    which.title("选取部分同学")
    which.geometry("850x720")  # 增大窗口高度以容纳人数选择
    which.transient(root)
    which.grab_set()
    
    selected_students = {}
    main_frame = ttk.Frame(which)
    main_frame.pack(fill='both', expand=True, padx=15, pady=15)
    
    title_label = tk.Label(main_frame, text="请选择同学", font=(FONT, 18, "bold"), fg=get_random_color())
    title_label.pack(pady=15)
    
    canvas = tk.Canvas(main_frame, bg='white')
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    row_counter = 0
    for group_idx, group in enumerate(student_list_group):
        group_label = tk.Label(scrollable_frame, text=f"第{group_idx + 1}组:", 
                              font=(FONT, 14, "bold"), fg=get_random_color())
        group_label.grid(row=row_counter, column=0, columnspan=4, sticky='w', pady=(20, 8), padx=15)
        row_counter += 1
        
        for i, student in enumerate(group):
            col = i % 4
            row = row_counter + (i // 4)
            
            var = tk.BooleanVar()
            selected_students[student] = var
            
            cb = tk.Checkbutton(scrollable_frame, text=student, variable=var,
                               font=(FONT, 12), bg='#F0F8FF', fg=get_random_color())
            cb.grid(row=row, column=col, sticky='w', padx=20, pady=5)
        
        row_counter += (len(group) + 3) // 4
    
    # 添加人数选择框架
    count_frame = tk.Frame(scrollable_frame, bg='white')
    count_frame.grid(row=row_counter, column=0, columnspan=4, pady=20, sticky='w', padx=15)
    row_counter += 1
    
    tk.Label(count_frame, text="抽取人数：", font=(FONT, 13)).grid(row=0, column=0, padx=10, pady=5)
    
    count_var = tk.StringVar(value=str(getattr(set_students, 'selected_count', 1)))  # 默认1人
    
    count_spinbox = ttk.Spinbox(count_frame, from_=1, to=42,  # 最大为全班人数
                               textvariable=count_var, width=8, font=(FONT, 13))
    count_spinbox.grid(row=0, column=1, padx=10, pady=5)
    
    # 人数提示标签
    count_info_label = tk.Label(count_frame, text=f"选择同学后可设置具体人数",
                               font=(FONT, 11), fg="#666666")
    count_info_label.grid(row=1, column=0, columnspan=2, pady=5, sticky='w')
    
    def update_spinbox_range():
        """根据选择的同学数量更新Spinbox的最大值"""
        selected_count = sum(1 for var in selected_students.values() if var.get())
        
        if selected_count > 0:
            count_spinbox.config(to=selected_count)
            count_info_label.config(text=f"最多可抽取{selected_count}人")
            
            # 确保当前值不超过最大值
            current_value = int(count_var.get())
            if current_value > selected_count:
                count_var.set(str(selected_count))
        else:
            count_spinbox.config(to=42)
            count_info_label.config(text="请先选择同学")
    
    # 初始更新一次
    update_spinbox_range()
    
    # 绑定选择变化事件
    for widget in scrollable_frame.winfo_children():
        if isinstance(widget, tk.Checkbutton):
            widget.config(command=update_spinbox_range)
    
    control_frame = tk.Frame(scrollable_frame, bg='white')
    control_frame.grid(row=row_counter, column=0, columnspan=4, pady=25)
    row_counter += 1
    
    def select_all():
        for var in selected_students.values():
            var.set(True)
        update_spinbox_range()
    
    def select_none():
        for var in selected_students.values():
            var.set(False)
        update_spinbox_range()
    
    tk.Button(control_frame, text="全选", command=select_all, 
              bg="#4ECDC4", fg="white", font=(FONT, 12), width=8, height=1).pack(side='left', padx=15)
    tk.Button(control_frame, text="全不选", command=select_none,
              bg="#FF6B6B", fg="white", font=(FONT, 12), width=8, height=1).pack(side='left', padx=15)
    
    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(fill='x', pady=15)
    
    result = []
    selected_count = 1
    
    def confirm_selection():
        nonlocal result, selected_count
        result = [student for student, var in selected_students.items() if var.get()]
        
        if not result:
            messagebox.showwarning("警告", "请至少选择一名同学！")
            return
        
        try:
            selected_count = int(count_var.get())
            if selected_count < 1 or selected_count > len(result):
                messagebox.showwarning("警告", f"抽取人数必须在1-{len(result)}之间！")
                return
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的数字！")
            return
        
        which.destroy()
    
    def cancel_selection():
        nonlocal result
        result = []
        which.destroy()
    
    tk.Button(button_frame, text="确定", command=confirm_selection,
              bg="#54A0FF", fg="white", font=(FONT, 14), width=10, height=1).pack(side='right', padx=15)
    tk.Button(button_frame, text="取消", command=cancel_selection,
              bg="#9E9E9E", fg="white", font=(FONT, 14), width=10, height=1).pack(side='right', padx=15)
    
    count_label = tk.Label(button_frame, text="已选择: 0 人", font=(FONT, 14), bg='white', fg="#FF6B6B")
    count_label.pack(side='left', padx=15)
    
    def update_count():
        count = sum(1 for var in selected_students.values() if var.get())
        count_label.config(text=f"已选择: {count} 人")
        which.after(100, update_count)
    
    update_count()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    which.wait_window(which)
    
    if result:
        set_students.selected_count = selected_count  # 保存选择的抽取人数
    return result

def group_select_window():
    """选择分组的窗口 - 支持多选"""
    group_win = tk.Toplevel(root)
    group_win.title("选择分组")
    group_win.geometry("600x600")  # 增大窗口高度以容纳多选控件
    group_win.transient(root)
    group_win.grab_set()
    
    main_frame = ttk.Frame(group_win)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    title_label = tk.Label(main_frame, text="选择分组", font=(FONT, 18, "bold"), fg=get_random_color())
    title_label.pack(pady=15)
    
    info_label = tk.Label(main_frame, text="请选择要抽取的组", font=(FONT, 12), fg="#666666")
    info_label.pack(pady=5)
    
    # 分组选择框架 - 改为多选框
    group_frame = tk.Frame(main_frame)
    group_frame.pack(pady=20)
    
    # 使用字典存储每个分组的选中状态
    group_vars = {}
    for i in range(6):
        group_vars[i+1] = tk.BooleanVar(value=(i+1 in current_groups))  # 默认选中当前分组

    gs_list = ["安梓萱", "刘苡歆", "宋禹良", "赵元祺", "周煜坤", "秦紫馨"]
    for i in range(6):
        cb = tk.Checkbutton(group_frame, text=f"{gs_list[i]}组", variable=group_vars[i+1],
                            font=(FONT, 13), fg=get_random_color(), bg='#F5F5F5')
        cb.grid(row=i//3, column=i%3, sticky='w', padx=25, pady=12)
    del gs_list
    
    # 人数选择框架
    count_frame = tk.Frame(main_frame)
    count_frame.pack(pady=20)
    
    tk.Label(count_frame, text="选择人数：", font=(FONT, 13)).grid(row=0, column=0, padx=10, pady=10)
    
    count_var = tk.StringVar(value=str(getattr(group_select_window, 'selected_count', 1)))  # 默认1人
    
    # 创建Spinbox，初始范围1-7
    count_spinbox = ttk.Spinbox(count_frame, from_=1, to=7, 
                                textvariable=count_var, width=8, font=(FONT, 13))
    count_spinbox.grid(row=0, column=1, padx=10, pady=10)
    
    # 人数提示标签
    count_info_label = tk.Label(count_frame, text=f"最多可抽取7人",
                                font=(FONT, 11), fg="#666666")
    count_info_label.grid(row=1, column=0, columnspan=2, pady=5)
    
    def update_spinbox_range():
        """根据选择的分组更新Spinbox的最大值"""
        selected_groups = [group_id for group_id, var in group_vars.items() if var.get()]
        
        if not selected_groups:
            # 如果没有选择任何分组，使用默认值
            count_spinbox.config(to=7)
            count_info_label.config(text="请选择要抽取的小组")
            return
            
        # 计算所有选中分组的总人数
        total_students = 0
        for group_id in selected_groups:
            group_idx = group_id - 1
            total_students += len(student_list_group[group_idx])
        
        count_spinbox.config(to=total_students)
        count_info_label.config(text=f"最多可抽取{total_students}人")
        
        # 确保当前值不超过最大值
        current_value = int(count_var.get())
        if current_value > total_students:
            count_var.set(str(total_students))
    
    # 初始更新一次
    update_spinbox_range()
    
    # 绑定组选择变化事件
    for widget in group_frame.winfo_children():
        if isinstance(widget, tk.Checkbutton):
            widget.config(command=update_spinbox_range)
    
    # 按钮框架
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill='x', pady=20)
    
    def confirm_group():
        global current_groups, selected_students_list
        current_groups = [group_id for group_id, var in group_vars.items() if var.get()]
        
        if not current_groups:
            messagebox.showwarning("警告", "请至少选择一个分组！")
            return
            
        # 保存选择的人数
        group_select_window.selected_count = int(count_var.get())
        # 清空已选择的学生列表，使用整个组
        selected_students_list = []
        group_win.destroy()
        update_status_display()
    
    def cancel_group():
        group_win.destroy()
    
    tk.Button(button_frame, text="确定", command=confirm_group,
              bg="#54A0FF", fg="white", font=(FONT, 14), width=10, height=1).pack(side='right', padx=15)
    tk.Button(button_frame, text="取消", command=cancel_group,
              bg="#9E9E9E", fg="white", font=(FONT, 14), width=10, height=1).pack(side='right', padx=15)
    
def set_students():
    global selected_students_list
    selected_students_list = which_window()
    if selected_students_list:  # 如果选择了学生，自动切换到分组模式
        set_mode(1)
    update_status_display()
    
# 在程序开始处添加
group_select_window.selected_count = 1  # 默认抽取1人
set_students.selected_count = 1  # 为选择同学模式也添加默认抽取人数

def count_window():
    """选择抽取数量的窗口"""
    count_win = tk.Toplevel(root)
    count_win.title("设置抽取数量")
    count_win.geometry("500x480")  # 增大窗口
    count_win.transient(root)
    count_win.grab_set()
    
    main_frame = ttk.Frame(count_win)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    title_label = tk.Label(main_frame, text="设置抽取数量", font=(FONT, 18, "bold"), fg=get_random_color())
    title_label.pack(pady=15)
    
    # 计算总学生数
    total_students = sum(len(group) for group in student_list_group)
    info_label = tk.Label(main_frame, text=f"全班共有 {total_students} 名同学", 
                         font=(FONT, 14), fg="#666666")
    info_label.pack(pady=10)
    
    # 数量选择框架
    count_frame = tk.Frame(main_frame)
    count_frame.pack(pady=30)
    
    tk.Label(count_frame, text="抽取数量：", font=(FONT, 14)).grid(row=0, column=0, padx=10, pady=15)
    
    count_var = tk.StringVar(value="1")
    count_spinbox = ttk.Spinbox(count_frame, from_=1, to=total_students, 
                               textvariable=count_var, width=12, font=(FONT, 14))
    count_spinbox.grid(row=0, column=1, padx=10, pady=15)
    
    # 快速选择按钮
    quick_frame = tk.Frame(main_frame)
    quick_frame.pack(pady=20)
    
    quick_counts = [1, 3, 5, 10]
    for i, count in enumerate(quick_counts):
        if count <= total_students:
            tk.Button(quick_frame, text=f"{count}人", font=(FONT, 12),
                     command=lambda c=count: count_var.set(str(c)),
                     bg="#FFEAA7", fg="#E17055", width=6).pack(side='left', padx=8)
    
    # 按钮框架
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill='x', pady=30)
    
    def confirm_count():
        try:
            count = int(count_var.get())
            if count < 1 or count > total_students:
                messagebox.showwarning("警告", f"数量必须在1-{total_students}之间！")
                return
            new_multiple_students.selected_count = count
            count_win.destroy()
            # 只设置数量，不自动开始抽取
            set_mode(2)
            update_status_display()
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的数字！")
    
    def cancel_count():
        new_multiple_students.selected_count = None
        count_win.destroy()
    
    tk.Button(button_frame, text="确定", command=confirm_count,
              bg="#54A0FF", fg="white", font=(FONT, 14), width=12).pack(side='right', padx=15)
    tk.Button(button_frame, text="取消", command=cancel_count,
              bg="#9E9E9E", fg="white", font=(FONT, 14), width=10).pack(side='right', padx=15)

def set_mode(new_mode):
    global mode, selected_students_list, current_groups

    if mode == new_mode: return

    mode = new_mode
    
    mode_names = ["全班模式", "分组模式", "数量模式"]
    mode_label.config(text=mode_names[mode])
    
    buttons = [all_class_button, group_button, count_button]
    for i, button in enumerate(buttons):
        if i == mode:
            button.config(bg=get_random_color(), fg="white", font=(FONT, 12, "bold"))
        else:
            button.config(bg="#E0E0E0", fg="#333333", font=(FONT, 12))
    
    # 更新主按钮
    if mode == 0:  # 全班模式
        selected_students_list.clear()
        new_student_button.config(text="开始抽取 🎯", command=new_student, bg="#FF6B6B")
    elif mode == 1:  # 分组模式
        new_student_button.config(text="开始抽取 🎯", command=new_student, bg="#4ECDC4")
    elif mode == 2:  # 数量模式
        new_student_button.config(text="按数量抽取 🔢", command=new_multiple_students, bg="#54A0FF")
    
    update_status_display()

def update_status_display():
    if mode == 0:
        status_label.config(text="状态: 将从全班同学中随机抽取1名同学", fg="#FF6B6B")
    elif mode == 1:  # 分组模式
        if selected_students_list:
            count = getattr(set_students, 'selected_count', 1)  # 获取选择的抽取人数
            if len(selected_students_list) <= 3:
                students_text = "、".join(selected_students_list)
                status_label.config(text=f"状态: 将从{students_text}中随机抽取{count}名同学", fg="#4ECDC4")
            else:
                status_label.config(text=f"状态: 将从{len(selected_students_list)}名同学中随机抽取{count}名同学", fg="#4ECDC4")
        else:
            if current_groups:
                count = getattr(group_select_window, 'selected_count', 1)  # 默认为1
                groups_text = "、".join([f"第{group}组" for group in current_groups])
                status_label.config(text=f"状态: 将从{groups_text}中随机抽取{count}名同学", fg="#4ECDC4")
            else:
                status_label.config(text=f"状态: 请选择要抽取的组", fg="#4ECDC4")
    elif mode == 2:  # 数量模式
        if hasattr(new_multiple_students, 'selected_count') and new_multiple_students.selected_count:
            count = new_multiple_students.selected_count
            status_label.config(text=f"状态: 将从全班抽取{count}名同学", fg="#54A0FF")
        else:
            status_label.config(text="状态: 请设置抽取数量", fg="#54A0FF")

def set_students():
    global selected_students_list
    selected_students_list = which_window()
    if selected_students_list:  # 如果选择了学生，自动切换到分组模式
        set_mode(1)
    update_status_display()

def set_group():
    group_select_window()
    # 选择分组后自动切换到分组模式
    set_mode(1)

def set_count():
    count_window()

global cleaned
cleaned = True

def clear_student_text():
    global cleaned
    if cleaned: return

    student_label.config(text="点击下方按钮开始抽取")
    clear_student_text_button.config(bg=get_random_color())

    cleaned = True

def objects():
    global mode_label, subject_label, student_label, new_student_button, clear_student_text_button
    global all_class_button, group_button, count_button, status_label, author_label, build_label

    try:
        bg_image = tk.PhotoImage(file="background.png")
        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except: pass

    root.configure(bg='#F5F5F5')

    build_label = tk.Label(root, text=f"版本号: v{build_num}", font=(FONT, 11), fg="#9d9d9d", bg='#F5F5F5')
    build_label.pack(anchor="nw", padx=10, pady=10)

    clear_student_text_button = tk.Button(root, text="清空", font=(FONT, 10), command=clear_student_text, bg=get_random_color(), fg="#232323")
    clear_student_text_button.place(relx=1.0, x=-150, y=20, anchor="ne")
    
    mode_label = tk.Label(root, text="全班模式", font=(FONT, 16), fg="#FF6B6B", bg='#F5F5F5')
    mode_label.place(relx=1.0, x=-40, y=20, anchor="ne")
    
    subject_label = tk.Label(root, text="随机同学 🎉", font=(FONT, 32, "bold"), fg=get_random_color(), bg='#F5F5F5')
    subject_label.pack(pady=(0, 30))
    
    student_label = tk.Label(root, text="点击下方按钮开始抽取", font=(FONT, 22), fg=get_random_color(), bg='#F5F5F5')
    student_label.pack(pady=(0, 20))
    
    status_label = tk.Label(root, text="状态: 将从全班同学中随机抽取1名同学",
                            font=(FONT, 13), fg="#FF6B6B", bg='#F5F5F5')
    status_label.pack(pady=(0, 25))
    
    new_student_button = tk.Button(root, text="开始抽取 🎯", font=(FONT, 18, "bold"),
                                   bg="#FF6B6B", fg="white", height=2, width=15,
                                   command=new_student)
    new_student_button.pack(pady=(10, 30))
    
    mode_frame = tk.Frame(root, bg='#F5F5F5')
    mode_frame.pack(pady=15)
    
    all_class_button = tk.Button(mode_frame, text="全班模式", font=(FONT, 13, "bold"),
                                bg="#FF6B6B", fg="white", width=12, height=2,
                                command=lambda: set_mode(0))
    all_class_button.pack(side='left', padx=8)
    
    group_button = tk.Button(mode_frame, text="分组模式", font=(FONT, 13),
                            bg="#E0E0E0", fg="#333333", width=12, height=2,
                            command=lambda: set_mode(1))
    group_button.pack(side='left', padx=8)
    
    count_button = tk.Button(mode_frame, text="数量模式", font=(FONT, 13),
                            bg="#E0E0E0", fg="#333333", width=12, height=2,
                            command=lambda: set_mode(2))
    count_button.pack(side='left', padx=8)
    
    setting_frame = tk.Frame(root, bg='#F5F5F5')
    setting_frame.pack(pady=20)
    
    group_setting_button = tk.Button(setting_frame, text="选择同学", font=(FONT, 12),
                                     bg="#4ECDC4", fg="white", width=12, height=1,
                                     command=set_students)
    group_setting_button.pack(side='left', padx=10)
    
    group_setting_button2 = tk.Button(setting_frame, text="选择分组", font=(FONT, 12),
                                     bg="#FF9FF3", fg="white", width=12, height=1,
                                     command=set_group)
    group_setting_button2.pack(side='left', padx=10)
    
    count_setting_button = tk.Button(setting_frame, text="设置数量", font=(FONT, 12),
                                     bg="#54A0FF", fg="white", width=12, height=1,
                                     command=set_count)
    count_setting_button.pack(side='left', padx=10)
    
    author_label = tk.Label(root, text="版权所有，侵权必究  2025 (c) 制作者：张程翔  @虾饼科技  保留所有权利",
                            font=(FONT, 11), fg="#9d9d9d", bg='#F5F5F5')
    author_label.pack(side="bottom", anchor="sw", padx=15, pady=10)

def main():
    objects()
    set_mode(0)
    root.mainloop()

if __name__ == "__main__":
    main()