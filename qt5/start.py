import sys
import PyQt5.sip
from PyQt5.QtWidgets import QApplication

from qt5.mainwindow import mainwindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mainwindow()
    w.show()
    sys.exit(app.exec_())
