from tkinter import *
from tkinter import scrolledtext
import threading
from icon import img
import base64


class GUI:
    wifi_tips = "无线模式依赖网络情况，建议在局域网信号较好的情况下使用。" \
                "\n密码和用户名如果是默认的可以不填" \
                "\n备注名可以让生成日志文件夹有新的名字" \
                "\n下载文件的顺序是从最新文件到最旧的文件，可以在恰当的时候停止下载"
    line_tips = "网线模式下,请正确手动设置电脑的ip" \
                "\n密码和用户名如果是默认的可以不填" \
                "\n备注名可以让生成日志文件夹有新的名字" \
                "\n下载文件的顺序是从最新文件到最旧的文件，可以在恰当的时候停止下载"

    def __init__(self, encode, decode):
        self.root_window = Tk()
        self.mode = IntVar()
        self.decode_text = StringVar()
        self.encode_text = StringVar()
        self.state = 0
        self.decode_callback = decode
        self.encode_callback = encode

        # UI
        self.canvas = None
        self.decode_before = None
        self.decode_result = None
        self.canvas_shape = None
        self.canvas_text = None
        self.canvas2 = None
        self.console_text2 = None
        self.canvas_shape2 = None
        self.canvas_text2 = None
        self.start_button_decode = None
        self.start_button_encode = None
        self.menu = None

    def start(self):
        self.root_window.mainloop()

    def execute_encode(self):
        text = self.decode_result.get('1.0', END)
        text = text.strip()
        result = self.encode_callback(text)
        self.append_encode_result_log(result)

    def execute_decode(self):
        text = self.decode_before.get('1.0', END)
        text = text.strip()
        result = self.decode_callback(text)
        self.append_decode_result_log(result)

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

        Receive = LabelFrame(self.root_window, text="接收区", padx=10, pady=10)
        Receive.grid(row=3, column=0, columnspan=9)
        self.decode_before = scrolledtext.ScrolledText(Receive,
                                                       width=40,
                                                       height=20, padx=8,
                                                       pady=10,
                                                       wrap=WORD)
        self.decode_before.grid(row=1, column=0)

        self.decode_result = scrolledtext.ScrolledText(Receive, width=40,
                                                       height=20, padx=8,
                                                       pady=10,
                                                       wrap=WORD)
        self.decode_result.grid(row=1, column=2)

        self.menu = LabelFrame(Receive, width=90, height=90)
        self.menu.grid(row=1, column=1)

        self.start_button_encode = Button(self.menu, text="<<加密", bg="lightblue", width=10,
                                          command=self.execute_encode)

        self.start_button_decode = Button(self.menu, text="解密>>", bg="lightblue", width=10,
                                          command=self.execute_decode)

        self.start_button_decode.grid(row=1, column=1, columnspan=2)
        self.start_button_encode.grid(row=2, column=1, rowspan=2)

    def update_log(self, log):
        thread = threading.Thread(target=self.append_log, args=(log,))
        thread.setDaemon(True)
        thread.start()

    def append_decode_result_log(self, log):
        self.decode_result.delete(1.0, END)
        self.decode_result.insert(END, log)
        self.decode_result.see(END)

    def append_encode_result_log(self, log):
        self.decode_before.delete(1.0, END)
        self.decode_before.insert(END, log)
        self.decode_before.see(END)
