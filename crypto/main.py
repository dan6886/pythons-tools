import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import PyQt5.sip
from crypto.untitled import Ui_MainWindow
from crypto.fuzzymacth import HashManager


class mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.helper = HashManager()
        self.setupUi(self)
        self.encry.clicked.connect(self.encry_click)
        self.decry.clicked.connect(self.decry_click)

    def encry_click(self):
        try:
            need_encry_text = self.left_text.toPlainText()
            self.helper.set_key(self.get_key())
            result = self.helper.get_aes_cfb(need_encry_text)
            print("encry:", need_encry_text)
            print("result:", result)
            self.right_text.setPlainText(result)
        except UnicodeDecodeError as  e:
            print(e)

        pass

    def decry_click(self):
        try:
            need_decry_text = self.right_text.toPlainText()
            self.helper.set_key(self.get_key())
            result = self.helper.back_aes_cfb(need_decry_text)
            print("decry:", need_decry_text)
            print("result:", result)
            self.left_text.setPlainText(result)
        except UnicodeDecodeError as e:
            print(e)
            self.left_text.setPlainText("[!!! 解密失败!!!]")
        pass

    def get_key(self):
        key_str = self.key.text()
        return key_str


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mainwindow()
    w.show()
    sys.exit(app.exec_())
