from tkinter import *
from tkinter import scrolledtext
import threading
from icon import img
import base64


class GUI:

    def __init__(self, start, stop):
        self.root_window = Tk()
        self.mode = IntVar()
        self.var_progress_bar_percent = StringVar()
        self.var_progress_bar_percent2 = StringVar()
        self.sum_length = 630
        self.start_callback = start
        self.stop_callback = stop
        self.ros_ip = StringVar()
        self.file_name = StringVar()
        self.user_name = StringVar()
        self.pass_word = StringVar()
        self.state = 0

    def start(self):
        self.root_window.mainloop()

    def excute(self):
        if self.state == 0:
            self.state = 1
            self.start_button['text'] = "停止"
            self.start_callback()
            self.console_text.delete(1.0, END)
        elif self.state == 1:
            self.state = 0
            self.start_button['text'] = "开始"
            self.update_progress_bar(0, "")
            self.update_progress_bar2(0, "")
            self.stop_callback()
            pass

    def stop(self):
        self.state = 0
        # self.callback()

    def set_init_window(self):
        self.root_window.geometry('780x481+10+10')
        self.root_window.title("wywbnjysxx")
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
        Radiobutton(self.root_window, variable=self.mode, text="无线模式", value=1, width=16,
                    command=self.mode_choose).grid(
            row=0,
            column=0)
        Radiobutton(self.root_window, variable=self.mode, text="网线模式", value=2, width=16,
                    command=self.mode_choose).grid(
            row=1,
            column=0)
        # IP地址
        # self.ros_ip.set('10.10.27.64')

        Label(self.root_window, text="RosIP:").grid(column=1, row=0, sticky='W')
        rosIp = Entry(self.root_window, width=15,
                      textvariable=self.ros_ip)
        rosIp.grid(column=2, row=0, sticky=W)
        rosIp.focus()
        # 文件夹备注
        Label(self.root_window, text="备注名:").grid(column=3, row=0, sticky='W')
        file_name_entry = Entry(self.root_window, width=15,
                                textvariable=self.file_name)
        file_name_entry.grid(column=4, row=0, sticky=W)
        file_name_entry.focus()

        # 用户名
        Label(self.root_window, text="用户名:").grid(column=5, row=0, sticky='W')
        userName = Entry(self.root_window, width=15,
                         textvariable=self.user_name)
        userName.grid(column=6, row=0, sticky=W)
        userName.focus()
        # 密码
        Label(self.root_window, text="密码:").grid(column=7, row=0, sticky='W')
        password = Entry(self.root_window, width=15,
                         textvariable=self.pass_word)
        password.grid(column=8, row=0, sticky=W)
        password.focus()

        Receive = LabelFrame(self.root_window, text="接收区", padx=10, pady=10)
        Receive.grid(row=3, column=0, columnspan=9)
        self.console_text = scrolledtext.ScrolledText(Receive, width=100, height=20, padx=8,
                                                      pady=10,
                                                      wrap=WORD)
        self.console_text.grid(row=3, column=0)

        # 进度条
        self.canvas = Canvas(self.root_window, width=600, height=26, bg="white")
        # 创建一个矩形外边框（距离左边，距离顶部，矩形宽度，矩形高度），线型宽度，颜色
        # self.out_line = self.canvas.create_rectangle(2, 2, 610, 27, width=1, outline="black")

        self.canvas_shape = self.canvas.create_rectangle(0, 0, 0, 0, fill='green')
        self.canvas_text = self.canvas.create_text(292, 4, anchor=NW)
        self.canvas.itemconfig(self.canvas_text, text='0%')
        self.var_progress_bar_percent.set('00.00  %')
        self.canvas.grid(row=1, column=1, columnspan=8, ipadx=5, sticky=E)

        # 总进度条
        self.canvas2 = Canvas(self.root_window, width=600, height=26, bg="white")
        self.canvas_shape2 = self.canvas2.create_rectangle(0, 0, 0, 0, fill='green')
        self.canvas_text2 = self.canvas2.create_text(292, 4, anchor=NW)
        self.canvas2.itemconfig(self.canvas_text2, text='0%')
        self.var_progress_bar_percent2.set('00.00  %')
        self.canvas2.grid(row=2, column=1, columnspan=8, ipadx=5, sticky=E)

        self.start_button = Button(self.root_window, text="开始", bg="lightblue", width=10,
                                   command=self.excute)
        self.start_button.grid(row=4, column=8)

    def mode_choose(self):
        mode = self.mode.get()
        if mode == 1:
            self.ros_ip.set("")
        elif mode == 2:
            self.ros_ip.set("192.168.11.123")
        print("" + str(self.mode.get()))

    def update_progress_bar(self, percent, msg):
        green_length = int(self.sum_length * percent / 100)
        self.canvas.coords(self.canvas_shape, (0, 0, green_length, 26))
        self.canvas.itemconfig(self.canvas_text, text='%s%%%s' % (percent, msg))
        self.var_progress_bar_percent.set('%0.2f  %%' % percent)

    def update_progress_bar2(self, percent, msg):
        green_length = int(self.sum_length * percent / 100)
        self.canvas2.coords(self.canvas_shape2, (0, 0, green_length, 26))
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
