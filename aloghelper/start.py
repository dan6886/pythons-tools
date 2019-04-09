from aloghelper.UI import GUI
from aloghelper.SSHHelper import SSHHelper
import threading


def start():
    print("start" + threading.current_thread().getName())
    thread = threading.Thread(target=ssh.start)
    thread.setDaemon(True)
    thread.start()
    pass


def stop():
    print("start" + threading.current_thread().getName())
    ssh.stop()
    pass


def clearAll():
    print("start" + threading.current_thread().getName())
    ssh.clearAll()
    pass


def open():
    print("start" + threading.current_thread().getName())
    ssh.open()
    pass


if __name__ == '__main__':
    ui = GUI(start, stop, clearAll, open)
    ui.set_init_window()
    ssh = SSHHelper()
    ssh.set_gui(ui)
    ui.start()
