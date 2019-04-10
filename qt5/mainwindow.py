import subprocess
import sys
import PyQt5.sip
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow

from qt5.uimain import Ui_MainWindow


class Worker(QThread):
    update_progress = pyqtSignal(str)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    notify_result = pyqtSignal(int, str)  # 自定义信号，执行run()函数时，从相关线程发射此信号
    notify_log = pyqtSignal(str)

    def __init__(self, parent=None, type=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0
        self.cmd = ""
        self.type = None

    def __del__(self):
        self.working = False
        # self.wait()

    def set_cmd(self, type, cmd):
        self.type = type
        self.cmd = cmd

    def run(self):
        print(self.type)
        if self.type == 1:
            # 拉取日志
            p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, universal_newlines=True,
                                 shell=True)
            for line in iter(p.stdout.readline, b''):
                if line == "" and p.poll() != None:
                    break

                line = line.rstrip()
                value = mainwindow.get_precent('[', ']', line)
                if value != 'node':
                    self.update_progress.emit(value)
                    print(">>>" + value)
            print("线程执行完成")
            mainwindow._status = 0
            self.notify_result.emit(self.type, None)
        elif self.type == 2:
            # 连接设备
            print("连接设备")
            p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, universal_newlines=True,
                                 shell=True)
            try:
                for line in iter(p.stdout.readline, b''):
                    if line == "" and p.poll() != None:
                        break

                    line = line.rstrip()
                    if line != "":
                        self.notify_log.emit(line)
                    print(">>>" + line)
            except UnicodeDecodeError as e:
                self.notify_log.emit("fail to connect")
            self.notify_result.emit(self.type, None)
        elif self.type == 3:
            # 生成日志
            p = subprocess.Popen("adb shell todo getlog 3", stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, universal_newlines=True,
                                 shell=True)
            for line in iter(p.stdout.readline, b''):
                if line == "" and p.poll() != None:
                    break

                line = line.rstrip()
                if line != "":
                    self.notify_log.emit(line)
                    mainwindow._last_log_name = mainwindow.get_log_name(line)
                print(">>>" + line)
            self.notify_result.emit(self.type, None)
            print("生成日志:")
        elif self.type == 4:
            # 生成日志
            p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, universal_newlines=True,
                                 shell=True)
            for line in iter(p.stdout.readline, b''):
                if line == "" and p.poll() != None:
                    break

                line = line.rstrip()
                if line != "":
                    self.notify_log.emit(line)
                    mainwindow._last_log_name = mainwindow.get_log_name(line)
                print(">>>" + line)
            self.notify_result.emit(self.type, None)
            print("删除全部:")
        elif self.type == 5:
            # 生成日志
            p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, universal_newlines=True,
                                 shell=True)
            for line in iter(p.stdout.readline, b''):
                if line == "" and p.poll() != None:
                    break

                line = line.rstrip()
                if line != "":
                    self.notify_log.emit(line)
                    mainwindow._last_log_name = mainwindow.get_log_name(line)
                print(">>>" + line)
            self.notify_result.emit(self.type, None)
            print("打开目录:")


class mainwindow(QMainWindow, Ui_MainWindow):
    _mode = "line"
    _aip = ""
    _add_name = ""
    _time = ""
    _child_dir = ""
    _last_log_name = ""
    _all_pull = False
    _status = 0

    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.start.clicked.connect(self.start_action)
        self.line.toggled.connect(lambda: self.raido_button_select("line"))
        self.wifi.toggled.connect(lambda: self.raido_button_select("wifi"))
        self.make_log.clicked.connect(self.make_log_action)
        self.all_pull.stateChanged.connect(self.all_pull_select)
        self.thread = Worker()
        self.thread.update_progress.connect(self.update_progress)
        self.thread.notify_result.connect(self.notify_result)
        self.thread.notify_log.connect(self.append_log)
        self.connectIp.clicked.connect(self.check_connect)
        self.clear_all.clicked.connect(self.clear)
        self.open_dir.clicked.connect(self.open)

    def start_action(self):
        if mainwindow._status != 0:
            self.append_log("当前正在执行任务，不可重复开始")
            return
        mainwindow._aip = self.aip.text()
        mainwindow._add_name = self.addname.text()
        mainwindow._time = self.hour.text()
        mainwindow._child_dir = self.child_dir.text()
        print('ip:{aip}|addname:{addname}|time:{time}|childdir:{childdir}|all_pll:{allpull}'.format(
            aip=mainwindow._aip,
            addname=mainwindow._add_name,
            time=mainwindow._time,
            childdir=mainwindow._child_dir,
            allpull=mainwindow._all_pull))
        self.check_dir()
        if mainwindow._all_pull:
            self.pull_file_all()
        else:
            self.pull_file_single()

    def check_dir(self):
        if mainwindow._child_dir != '':
            self.mkdir(mainwindow._child_dir)

    def check_connect(self):
        mainwindow._aip = self.aip.text()
        print("log make")
        # if mainwindow._status != 0:
        #     self.append_log("当前正在执行任务，不可重复开始")
        #     print("重复了")
        #     return
        mainwindow._status = 2
        cmd = 'adb connect {ip}'.format(ip=mainwindow._aip)
        self.append_log(cmd)
        self.thread.set_cmd(2, cmd)
        self.thread.start()

    def notify_result(self, typeint, result):
        print(typeint, result)
        if typeint == 1:
            mainwindow._status = 0
            pass
        elif typeint == 2:
            mainwindow._status = 0
            pass
        elif typeint == 3:
            mainwindow._status = 0

        mainwindow._status = 0

    def make_log_action(self):
        time = self.hour.text()
        mainwindow._time = time
        if time == '':
            mainwindow._time = '8'

        if mainwindow._status != 0:
            self.append_log("当前正在执行任务，不可重复开始")
            print("重复了")
            return
        mainwindow._status = 3
        cmd = 'adb shell todo getlog {hour}'.format(hour=mainwindow._time)
        self.append_log(cmd)
        self.thread.set_cmd(3, cmd)
        self.thread.start()
        pass

    @staticmethod
    def get_log_name(str_name):
        if str_name.startswith('/sdcard/log/Alog'):
            file_name = str_name.split("/")[-1].strip("\n")
            print("日志名称:" + file_name)
            return file_name
        return None

    def raido_button_select(self, name):
        target = self.sender()
        if not target.isChecked():
            return
        mainwindow._mode = name

        print("name:" + mainwindow._mode)
        pass

    def all_pull_select(self):
        target = self.sender()
        mainwindow._all_pull = target.isChecked()

    def stop_action(self):
        pass

    def append_log(self, text):
        self.log_text.append(text)
        # self.log_text.append("\n")
        pass

    def update_progress(self, value):
        self.progress.setValue(int(value))
        pass

    def pull_file_single(self):
        cmd = 'adb pull /sdcard/log/{old_name} ./{dir_child}/{append_name}{old_name}'.format(
            old_name=mainwindow._last_log_name,
            dir_child=mainwindow._child_dir,
            append_name=mainwindow._add_name)
        self.pull_file(cmd=cmd)

    def pull_file_all(self):
        cmd = 'adb pull /sdcard/log/ ./{dir_child}'.format(dir_child=mainwindow._child_dir)
        self.pull_file(cmd=cmd)

    def pull_file(self, cmd):
        mainwindow._status = 2
        self.append_log(cmd)
        self.thread.set_cmd(1, cmd)
        self.thread.start()
        print("拉取开启线程:")

    def do_real_pull(self, cmd):
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True,
                             shell=True)

        for line in iter(p.stdout.readline, b''):
            if line == "" and p.poll() != None:
                break

            line = line.rstrip()
            value = mainwindow.get_precent('[', ']', line)
            if value != 'node':
                self.update_progress(value)
                print(">>>" + value)
        print("线程执行完成")
        mainwindow._status = 0

    def clear(self):
        mainwindow._status = 4
        cmd = "adb shell rm -rf /sdcard/log/*"
        self.append_log(cmd)
        self.thread.set_cmd(4, cmd)
        self.thread.start()
        pass

    def open(self):
        mainwindow._status = 5
        cmd = "start ."
        self.append_log(cmd)
        self.thread.set_cmd(5, cmd)
        self.thread.start()
        pass

    @staticmethod
    def get_precent(start_str, end, thestr):
        start = thestr.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = thestr.find(end, start)
            if end >= 0:
                return thestr[start:end].strip().replace("%", "")
        return "node"

    def mkdir(self, path):
        # 引入模块
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            os.makedirs(path)
            print(path + ' 创建成功')
            self.append_log(path + '---->创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            self.append_log(path + '---->目录已存在')
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mainwindow()
    w.show()
    sys.exit(app.exec_())
