# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'motorui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 645)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 200, 361, 321))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 361, 194))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.port_select = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.port_select.sizePolicy().hasHeightForWidth())
        self.port_select.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.port_select.setFont(font)
        self.port_select.setObjectName("port_select")
        self.gridLayout_2.addWidget(self.port_select, 0, 0, 1, 1)
        self.open_serial = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_serial.sizePolicy().hasHeightForWidth())
        self.open_serial.setSizePolicy(sizePolicy)
        self.open_serial.setMinimumSize(QtCore.QSize(56, 56))
        self.open_serial.setMaximumSize(QtCore.QSize(100, 201))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.open_serial.setFont(font)
        self.open_serial.setObjectName("open_serial")
        self.gridLayout_2.addWidget(self.open_serial, 0, 1, 2, 1)
        self.baund_rate = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baund_rate.sizePolicy().hasHeightForWidth())
        self.baund_rate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.baund_rate.setFont(font)
        self.baund_rate.setObjectName("baund_rate")
        self.baund_rate.addItem("")
        self.baund_rate.addItem("")
        self.baund_rate.addItem("")
        self.baund_rate.addItem("")
        self.baund_rate.addItem("")
        self.gridLayout_2.addWidget(self.baund_rate, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.forward_vol = QtWidgets.QComboBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.forward_vol.setFont(font)
        self.forward_vol.setObjectName("forward_vol")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.forward_vol.addItem("")
        self.gridLayout.addWidget(self.forward_vol, 0, 0, 1, 1)
        self.backward_vol = QtWidgets.QComboBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.backward_vol.setFont(font)
        self.backward_vol.setObjectName("backward_vol")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.backward_vol.addItem("")
        self.gridLayout.addWidget(self.backward_vol, 0, 1, 1, 1)
        self.motor_forward = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.motor_forward.setFont(font)
        self.motor_forward.setObjectName("motor_forward")
        self.gridLayout.addWidget(self.motor_forward, 1, 0, 1, 1)
        self.motor_backward = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.motor_backward.setFont(font)
        self.motor_backward.setObjectName("motor_backward")
        self.gridLayout.addWidget(self.motor_backward, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.forward_time = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forward_time.sizePolicy().hasHeightForWidth())
        self.forward_time.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.forward_time.setFont(font)
        self.forward_time.setObjectName("forward_time")
        self.gridLayout.addWidget(self.forward_time, 3, 0, 1, 1)
        self.backward_time = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backward_time.sizePolicy().hasHeightForWidth())
        self.backward_time.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.backward_time.setFont(font)
        self.backward_time.setObjectName("backward_time")
        self.gridLayout.addWidget(self.backward_time, 3, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.textBrowser = QtWidgets.QTextBrowser(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 451, 18))
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
        self.groupBox.setTitle(_translate("MainWindow", "Graph"))
        self.open_serial.setText(_translate("MainWindow", "打开\n"
"串口"))
        self.baund_rate.setItemText(0, _translate("MainWindow", "1382400"))
        self.baund_rate.setItemText(1, _translate("MainWindow", "115200"))
        self.baund_rate.setItemText(2, _translate("MainWindow", "38400"))
        self.baund_rate.setItemText(3, _translate("MainWindow", "19200"))
        self.baund_rate.setItemText(4, _translate("MainWindow", "9600"))
        self.forward_vol.setItemText(0, _translate("MainWindow", "12V"))
        self.forward_vol.setItemText(1, _translate("MainWindow", "11V"))
        self.forward_vol.setItemText(2, _translate("MainWindow", "10V"))
        self.forward_vol.setItemText(3, _translate("MainWindow", "9V"))
        self.forward_vol.setItemText(4, _translate("MainWindow", "8V"))
        self.forward_vol.setItemText(5, _translate("MainWindow", "7V"))
        self.forward_vol.setItemText(6, _translate("MainWindow", "6V"))
        self.forward_vol.setItemText(7, _translate("MainWindow", "5V"))
        self.forward_vol.setItemText(8, _translate("MainWindow", "4V"))
        self.forward_vol.setItemText(9, _translate("MainWindow", "3V"))
        self.backward_vol.setItemText(0, _translate("MainWindow", "12V"))
        self.backward_vol.setItemText(1, _translate("MainWindow", "11V"))
        self.backward_vol.setItemText(2, _translate("MainWindow", "10V"))
        self.backward_vol.setItemText(3, _translate("MainWindow", "9V"))
        self.backward_vol.setItemText(4, _translate("MainWindow", "8V"))
        self.backward_vol.setItemText(5, _translate("MainWindow", "7V"))
        self.backward_vol.setItemText(6, _translate("MainWindow", "6V"))
        self.backward_vol.setItemText(7, _translate("MainWindow", "5V"))
        self.backward_vol.setItemText(8, _translate("MainWindow", "4V"))
        self.backward_vol.setItemText(9, _translate("MainWindow", "3V"))
        self.motor_forward.setText(_translate("MainWindow", "正转"))
        self.motor_backward.setText(_translate("MainWindow", "反转"))
        self.label.setText(_translate("MainWindow", "正转时间"))
        self.label_2.setText(_translate("MainWindow", "反转时间"))