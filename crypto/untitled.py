# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.txt'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(791, 517)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 771, 461))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_text = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.left_text.setObjectName("left_text")
        self.horizontalLayout.addWidget(self.left_text)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.encry = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.encry.setObjectName("encry")
        self.verticalLayout.addWidget(self.encry)
        self.key = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key.sizePolicy().hasHeightForWidth())
        self.key.setSizePolicy(sizePolicy)
        self.key.setMinimumSize(QtCore.QSize(5, 10))
        self.key.setMaximumSize(QtCore.QSize(200, 16777215))
        self.key.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.key.setObjectName("key")
        self.verticalLayout.addWidget(self.key)
        self.decry = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.decry.setObjectName("decry")
        self.verticalLayout.addWidget(self.decry)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.right_text = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.right_text.setObjectName("right_text")
        self.horizontalLayout.addWidget(self.right_text)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 791, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.encry.setText(_translate("MainWindow", "加密>>"))
        self.key.setPlaceholderText(_translate("MainWindow", "采用默认密钥或输入"))
        self.decry.setText(_translate("MainWindow", "<<解密"))


