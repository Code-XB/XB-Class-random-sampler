import tkinter as tk
import time
import random
from datetime import datetime

FONT = "微软雅黑"
mode = 0  # 0:正计时, 1:倒计时, 2:实际时间
running = False
start_time = 0
elapsed_time = 0
countdown_time = 300  # 默认5分钟倒计时（300秒）
pause_time = 0  # 用于记录暂停的时间点

# 创建主窗口
root = tk.Tk()
root.geometry("350x480")
root.title("多功能计时器")
root.resizable(False, False)

def get_random_color():
    """生成更鲜艳的随机颜色"""
    bright_colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#FF9FF3', '#54A0FF',
        '#5F27CD', '#00D2D3', '#FF9F43', '#10AC84', '#EE5A24',
        '#A3CB38', '#1289A7', '#D980FA', '#B53471', '#FFC312'
    ]
    return random.choice(bright_colors)

def update_display():
    """更新时间显示"""
    if mode == 0:  # 正计时模式
        if running:
            elapsed = time.time() - start_time + elapsed_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    elif mode == 1:  # 倒计时模式
        if running:
            remaining = countdown_time - (time.time() - start_time)
            if remaining <= 0:
                time_label.config(text="00:00:00")
                stop()
                # 播放提示音（这里用改变背景色代替）
                root.config(bg='#FF6B6B')
                root.after(500, lambda: root.config(bg='SystemButtonFace'))
                root.after(1000, lambda: root.config(bg='#FF6B6B'))
                root.after(1500, lambda: root.config(bg='SystemButtonFace'))
                status_label.config(text="倒计时结束！", fg='red')
                return
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            seconds = int(remaining % 60)
            time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            hours = int(countdown_time // 3600)
            minutes = int((countdown_time % 3600) // 60)
            seconds = int(countdown_time % 60)
            time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    elif mode == 2:  # 实际时间模式
        current_time = datetime.now().strftime("%H:%M:%S")
        time_label.config(text=current_time)
        if running:
            status_label.config(text="实时时间自动更新中", fg='green')
        else:
            status_label.config(text="点击开始更新实时时间", fg='gray')
    
    # 每100毫秒更新一次
    root.after(100, update_display)

def start_pause():
    """开始/暂停计时"""
    global running, start_time, elapsed_time, countdown_time, pause_time
    
    if not running:
        # 开始计时
        running = True
        start_time = time.time()
        if mode == 0:  # 正计时
            status_label.config(text="正计时进行中...", fg='green')
        elif mode == 1:  # 倒计时
            status_label.config(text="倒计时进行中...", fg='orange')
        elif mode == 2:  # 实际时间
            status_label.config(text="实时时间自动更新中", fg='green')
        start_pause_btn.config(text="暂停", fg='red', bg='#FF6B6B')
        reset_btn.config(state='normal')
    else:
        # 暂停计时
        stop()

def stop():
    """暂停计时"""
    global running, elapsed_time, countdown_time, pause_time
    if running:
        running = False
        pause_time = time.time()
        
        if mode == 0:  # 正计时
            elapsed_time += pause_time - start_time
            status_label.config(text="已暂停", fg='gray')
        elif mode == 1:  # 倒计时
            countdown_time -= pause_time - start_time
            if countdown_time < 0:
                countdown_time = 0
            status_label.config(text="已暂停", fg='gray')
        elif mode == 2:  # 实际时间
            status_label.config(text="已暂停更新", fg='gray')
        
        start_pause_btn.config(text="继续", fg='green', bg='#4ECDC4')

def reset():
    """重置计时器"""
    global running, elapsed_time, countdown_time
    running = False
    
    if mode == 0:  # 正计时
        elapsed_time = 0
        time_label.config(text="00:00:00")
        status_label.config(text="点击'开始'按钮开始正计时", fg='gray')
    elif mode == 1:  # 倒计时
        # countdown_time 保持不变，保持用户设置的值
        hours = int(countdown_time // 3600)
        minutes = int((countdown_time % 3600) // 60)
        seconds = int(countdown_time % 60)
        time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        status_label.config(text="点击'开始'按钮开始倒计时", fg='gray')
    elif mode == 2:  # 实际时间
        current_time = datetime.now().strftime("%H:%M:%S")
        time_label.config(text=current_time)
        status_label.config(text="点击'开始'按钮开始更新实时时间", fg='gray')
    
    start_pause_btn.config(text="开始", fg='green', bg='#4ECDC4')
    reset_btn.config(state='disabled')

def set_mode(new_mode):
    """切换模式"""
    global mode, running, elapsed_time, countdown_time
    running = False
    mode = new_mode
    
    # 更新按钮状态
    start_pause_btn.config(text="开始", fg='green', bg='#4ECDC4')
    reset_btn.config(state='disabled')
    
    # 更新模式标签颜色
    for i, btn in enumerate(mode_buttons):
        if i == new_mode:
            btn.config(fg='white', bg='#2C3E50', font=(FONT, 12, 'bold'))
        else:
            btn.config(fg='black', bg='SystemButtonFace', font=(FONT, 12))
    
    # 更新标题
    titles = ["正计时", "倒计时", "实际时间"]
    subject_label.config(text=titles[new_mode], fg=get_random_color())
    
    # 更新倒计时设置按钮的显示状态
    if new_mode == 1:  # 倒计时模式
        countdown_set_btn.pack(pady=5)
    else:
        countdown_set_btn.pack_forget()
    
    # 重置并更新显示
    reset()
    update_display()

def set_countdown():
    """设置倒计时时间"""
    def apply_time():
        try:
            global countdown_time, running
            minutes = int(time_entry.get())
            if 1 <= minutes <= 999:
                countdown_time = minutes * 60
                reset()  # 重置计时器
                set_window.destroy()
                status_label.config(text=f"已设置为{minutes}分钟倒计时", fg='blue')
            else:
                tk.messagebox.showerror("错误", "请输入1-999之间的数字")
        except ValueError:
            tk.messagebox.showerror("错误", "请输入有效的数字")
    
    set_window = tk.Toplevel(root)
    set_window.title("设置倒计时")
    set_window.geometry("250x150")
    set_window.resizable(False, False)
    
    tk.Label(set_window, text="设置倒计时时间（分钟）", font=(FONT, 12)).pack(pady=10)
    
    time_entry = tk.Entry(set_window, font=(FONT, 14), width=10, justify='center')
    time_entry.pack(pady=10)
    time_entry.insert(0, str(int(countdown_time // 60)))
    time_entry.focus()
    time_entry.select_range(0, tk.END)
    
    tk.Button(set_window, text="确定", font=(FONT, 12), command=apply_time, 
              bg='#4ECDC4', fg='white', width=10).pack(pady=10)

# 标题
subject_label = tk.Label(root, text="正计时", font=(FONT, 25), fg=get_random_color())
subject_label.pack(pady=(20, 10))

# 时间显示
time_label = tk.Label(root, font=(FONT, 40, 'bold'), fg='#2C3E50', 
                      text="00:00:00", width=10, height=2, bg='#F0F0F0',
                      relief='ridge', bd=3)
time_label.pack(pady=10)

# 控制按钮框架
control_frame = tk.Frame(root)
control_frame.pack(pady=20)

# 开始/暂停按钮（合并功能）
start_pause_btn = tk.Button(control_frame, text="开始", font=(FONT, 14), 
                           width=8, height=2, command=start_pause, 
                           bg='#4ECDC4', fg='white', activebackground='#45B7D1')
start_pause_btn.pack(side=tk.LEFT, padx=5)

# 重置按钮
reset_btn = tk.Button(control_frame, text="重置", font=(FONT, 14), 
                      width=8, height=2, command=reset, bg='#FF9F43', fg='white',
                      state='disabled', activebackground='#EE5A24')
reset_btn.pack(side=tk.LEFT, padx=5)

# 模式选择框架
mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)

mode_buttons = []
modes = ["正计时", "倒计时", "实际时间"]

for i, mode_text in enumerate(modes):
    btn = tk.Button(mode_frame, text=mode_text, font=(FONT, 12), 
                    width=8, command=lambda m=i: set_mode(m))
    btn.pack(side=tk.LEFT, padx=5)
    mode_buttons.append(btn)

# 倒计时设置按钮（只在倒计时模式下显示）
countdown_set_btn = tk.Button(root, text="设置倒计时时间", font=(FONT, 10), 
                              command=set_countdown, bg='#DDA0DD', fg='white',
                              activebackground='#C154C1')

# 状态标签
status_label = tk.Label(root, text="点击'开始'按钮开始计时", 
                        font=(FONT, 10), fg='gray')
status_label.pack(pady=10)

# 底部信息标签
info_label = tk.Label(root, text="计时器 v1.0", font=(FONT, 8), fg='lightgray')
info_label.pack(side=tk.BOTTOM, pady=5)

# 设置初始模式
set_mode(0)

# 启动显示更新
update_display()

# 运行主循环
if __name__ == "__main__":
    root.mainloop()