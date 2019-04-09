from tkinter import *
from tkinter import scrolledtext
import threading
from icon import img
import base64


class GUI:
    wifi_tips = "无线模式依赖网络情况，建议在局域网信号较好的情况下使用。请填写Android设备的ip地址" \
                "\n备注名可以拼接到生成的日志文件名称前面------可以中文" \
                "\n默认时间为8小时" \
                "\n子文件夹可以把生成的日志存到子文件夹里面" \
                "\n如果需要拉取全部日志，都切换按钮即可"
    line_tips = "数据线模式下,ip可以不用管" \
                "\n备注名可以拼接到生成的日志文件名称前面-------可以中文" \
                "\n默认时间为8小时" \
                "\n子文件夹可以把生成的日志存到子文件夹里面-----避免中文" \
                "\n如果需要拉取全部日志，都切换按钮即可"

    def __init__(self, start, stop, clearAll, open):
        self.root_window = Tk()
        self.mode = IntVar()
        self.pull_mode = IntVar()
        self.var_progress_bar_percent = StringVar()
        self.var_progress_bar_percent2 = StringVar()
        self.sum_length = 630
        self.start_callback = start
        self.stop_callback = stop
        self.clear_callback = clearAll
        self.open_callback = open
        self.android_ip = StringVar()
        self.file_name = StringVar()
        self.log_time = StringVar()
        self.dir_child = StringVar()
        self.state = 0
        # UI
        self.canvas = None
        self.console_text = None
        self.canvas_shape = None
        self.canvas_text = None
        self.canvas2 = None
        self.console_text2 = None
        self.canvas_shape2 = None
        self.canvas_text2 = None
        self.start_button = None
        self.clear_button = None
        self.open_button = None

    def start(self):
        self.root_window.mainloop()

    def execute(self):
        if self.state == 0:
            self.state = 1
            self.start_button['text'] = "停止"
            self.console_text.delete(1.0, END)
            self.start_callback()

        elif self.state == 1:
            self.state = 0
            self.start_button['text'] = "开始"
            self.stop_callback()
            pass

    def clear(self):
        self.clear_callback()

    def open(self):
        self.open_callback()

    def stop(self):
        self.state = 0
        # self.callback()

    def set_init_window(self):
        self.root_window.geometry('780x481+10+10')
        self.root_window.title("i l coco g")
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.root_window.iconbitmap("tmp.ico")
        # os.remove("tmp.ico")

        # self.root_window.iconbitmap('icon/123.ico')
        button = Button(self.root_window, text="❤")
        button.grid(row=1, column=1)
        button.place(x=100, y=100)
        self.mode.set(1)
        Radiobutton(self.root_window, variable=self.mode, text="数据线模式", value=1, width=16,
                    command=self.mode_choose).grid(
            row=0,
            column=0)
        Radiobutton(self.root_window, variable=self.mode, text="无线模式", value=2, width=16,
                    command=self.mode_choose).grid(
            row=1,
            column=0)
        self.pull_mode.set(1)

        Radiobutton(self.root_window, variable=self.pull_mode, text="只拉取本次日志", value=1, width=16,
                    command=self.pull_mode_choose).grid(
            row=4,
            column=5)
        Radiobutton(self.root_window, variable=self.pull_mode, text="拉取全部日志", value=2, width=16,
                    command=self.pull_mode_choose).grid(
            row=4,
            column=6)
        # IP地址
        # self.ros_ip.set('10.10.27.64')

        Label(self.root_window, text="AndroidIP:").grid(column=1, row=0, sticky='W')
        rosIp = Entry(self.root_window, width=15,
                      textvariable=self.android_ip)
        rosIp.grid(column=2, row=0, sticky=W)
        rosIp.focus()
        # 文件夹备注
        Label(self.root_window, text="日志备注名:").grid(column=3, row=0, sticky='W')
        file_name_entry = Entry(self.root_window, width=15,
                                textvariable=self.file_name)
        file_name_entry.grid(column=4, row=0, sticky=W)
        file_name_entry.focus()

        # 抓取时间
        Label(self.root_window, text="时间/h:").grid(column=1, row=1, sticky='W')
        userName = Entry(self.root_window, width=15,
                         textvariable=self.log_time)
        userName.grid(column=2, row=1, sticky=W)
        userName.focus()
        # 子文件夹
        Label(self.root_window, text="子文件夹:").grid(column=3, row=1, sticky='W')
        password = Entry(self.root_window, width=15,
                         textvariable=self.dir_child)
        password.grid(column=4, row=1, sticky=W)
        password.focus()

        Receive = LabelFrame(self.root_window, text="接收区", padx=10, pady=10)
        Receive.grid(row=3, column=0, columnspan=9)
        self.console_text = scrolledtext.ScrolledText(Receive, width=100, height=20, padx=8,
                                                      pady=10,
                                                      wrap=WORD)
        self.console_text.grid(row=3, column=0)

        # # 进度条
        # self.canvas = Canvas(self.root_window, width=600, height=26, bg="white")
        # # 创建一个矩形外边框（距离左边，距离顶部，矩形宽度，矩形高度），线型宽度，颜色
        #
        # self.canvas_shape = self.canvas.create_rectangle(0, 0, 0, 0, fill='green', width=0)
        # self.canvas_text = self.canvas.create_text(292, 4, anchor=NW)
        # self.canvas.itemconfig(self.canvas_text, text='0%')
        # self.var_progress_bar_percent.set('00.00  %')
        # self.canvas.grid(row=1, column=1, columnspan=4, ipadx=5, sticky=E)
        #
        # # 总进度条
        # self.canvas2 = Canvas(self.root_window, width=600, height=26, bg="white")
        # self.canvas_shape2 = self.canvas2.create_rectangle(0, 0, 0, 0, fill='green', width=0)
        # self.canvas_text2 = self.canvas2.create_text(292, 4, anchor=NW)
        # self.canvas2.itemconfig(self.canvas_text2, text='0%')
        # self.var_progress_bar_percent2.set('00.00  %')
        # self.canvas2.grid(row=2, column=1, columnspan=4, ipadx=5, sticky=E)

        self.start_button = Button(self.root_window, text="开始", bg="lightblue", width=10,
                                   command=self.execute)
        self.start_button.grid(row=4, column=4)

        self.clear_button = Button(self.root_window, text="清除日志", bg="lightblue", width=10,
                                   command=self.clear)
        self.clear_button.grid(row=4, column=3)

        self.open_button = Button(self.root_window, text="打开目录", bg="lightblue", width=10,
                                  command=self.open)
        self.open_button.grid(row=4, column=2)

        self.update_log(GUI.line_tips)
        self.log_time.set("8")

    def mode_choose(self):
        mode = self.mode.get()
        if mode == 1:
            self.android_ip.set("")
            if self.state == 0:
                self.console_text.delete(1.0, END)
                self.append_log(GUI.wifi_tips)
        elif mode == 2:
            self.android_ip.set("10.10.61.177")
            if self.state == 0:
                self.console_text.delete(1.0, END)
                self.append_log(GUI.line_tips)
        print("" + str(self.mode.get()))

    def pull_mode_choose(self):
        pull_mode = self.pull_mode.get()
        if pull_mode == 1:
            if self.state == 0:
                self.append_log("只拉取本次生成的日志")
        elif pull_mode == 2:
            if self.state == 0:
                self.append_log("拉取设备端存放的全部日志")

    def update_progress_bar(self, percent, msg):
        if percent >= 100:
            percent = 100
        green_length = int(self.sum_length * percent / 100)
        self.canvas.coords(self.canvas_shape, (0, 3, green_length, 27))
        self.canvas.itemconfig(self.canvas_text, text='%s%%%s' % (percent, msg))
        self.var_progress_bar_percent.set('%0.2f  %%' % percent)

    def update_progress_bar2(self, percent, msg):
        if percent >= 100:
            percent = 100
        green_length = int(self.sum_length * percent / 100)
        self.canvas2.coords(self.canvas_shape2, (0, 3, green_length, 27))
        self.canvas2.itemconfig(self.canvas_text2, text='%s%%%s' % (percent, msg))
        self.var_progress_bar_percent2.set('%0.2f  %%' % percent)

    def finish(self):
        if self.state == 1:
            self.state = 0
            self.start_button['text'] = "开始"

    def update_log(self, log):
        thread = threading.Thread(target=self.append_log, args=(log,))
        thread.setDaemon(True)
        thread.start()

    def append_log(self, log):
        self.console_text.insert(END, log + "\n")
        self.console_text.see(END)
