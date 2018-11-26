from ui.UI import GUI
from ui.SSHHelper import SSHHelper
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


if __name__ == '__main__':
    ui = GUI(start, stop)
    ui.set_init_window()
    ssh = SSHHelper()
    ssh.set_gui(ui)
    ui.start()
