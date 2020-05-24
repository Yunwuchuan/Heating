# -*- coding: utf-8 -*-
# Author：Tang XT
# Time: 2020/5/21/21:17
# File name：runmainwindow.py

import sys
import motorui
from mycode import globalvar as gl
from mycode.myserial import *
import threading


from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QWidget, QAction, QGridLayout
from PyQt5 import QtCore,  QtGui
import pyqtgraph as pg


class Binding(QWidget):
    def __init__(self, ui, mainwindow):
        super(QWidget, self).__init__()
        self.ui = ui
        self.mainwindow = mainwindow
        self.count = 0
        self.port_state = 0

        #串口选择栏
        self.ui.port_select.addItem("Refresh")
        self.ui.port_select.insertSeparator(1)
        self.ui.port_select.setCurrentIndex(-1)
        self.ui.port_select.activated.connect(self.re_serial_port)
        #------

        #波特率选择栏
        self.ui.baund_rate.setCurrentIndex(-1)
        #-------

        #打开串口按钮
        self.ui.open_serial.clicked.connect(self.openSerial)
        self.ui.open_serial.setCheckable(True)
        #---------

        #正转按钮
        self.ui.motor_forward.pressed.connect(self.motor_move)
        self.ui.motor_forward.released.connect(self.motor_stop)

        #反转按钮
        self.ui.motor_backward.pressed.connect(self.motor_move)
        self.ui.motor_backward.released.connect(self.motor_stop)

        #定时器
        self.time = QtCore.QTimer(self)
        self.time.setInterval(100)
        self.time.timeout.connect(self.time_refresh)

        self.grid = QGridLayout()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pw = pg.PlotWidget(title = "test")
        pw.showGrid(x=True, y=True)
        pw.setLabel('left', "Y Axis", units='A')
        pw.setLabel('bottom', "X Axis", units='s')
        # pw.showAxis('right',True)
        # pw.showAxis('top',True)
        #
        self.grid.addWidget(pw,0,0)
        # pw1 = pg.PlotWidget()
        # self.grid.addWidget(pw1, 0, 1)
        # pw2 = pg.PlotWidget()
        # self.grid.addWidget(pw2, 1, 0)
        # pw3 = pg.PlotWidget()
        # self.grid.addWidget(pw3, 1, 1)
        self.ui.groupBox.setLayout(self.grid)

        pw.plot([1,2,3],[2,4,6],pen=(255,0,0), name="Red curve")
        pw.plot([1,2,3],[3,6,9],pen=(0,255,0), name="Green curve")


    def re_serial_port(self, index):

        def setPortlist():
            self.ui.port_select.clear()
            self.ui.port_select.addItem("Refresh")
            self.ui.port_select.insertSeparator(1)
            self.ui.port_select.setEnabled(False)
            scan_serialport()
            for item in gl.port_list:
                self.ui.port_select.addItem(item)
            self.ui.port_select.setCurrentIndex(-1)
            self.ui.port_select.setEnabled(True)

        if index == 0:
            newthread = threading.Thread(target= setPortlist)
            newthread.start()

    def openSerial(self):
        if self.ui.open_serial.isChecked():

            gl.mainserial = Myserial(self.ui.port_select.currentText().split(" ")[0], \
                                         int(self.ui.baund_rate.currentText()), timeout=None, textbox=self.ui.textBrowser, queue=gl.queue1)

            try:
                self.port_state = gl.mainserial.is_open
            except:
                self.port_state = 0
            if self.port_state:
                self.ui.open_serial.setText("关闭\n串口")
                self.ui.open_serial.setChecked(True)
                gl.mainserial.start_loop()

        else:
            gl.mainserial.close()
            try:
                self.port_state = gl.mainserial.is_open
            except:
                self.port_state = 0

            if not self.port_state:
                self.ui.open_serial.setText("打开\n串口")
                self.ui.open_serial.setChecked(False)

    def motor_move(self):
        self.time.start()
        if self.port_state:
            sender = self.mainwindow.sender()
            if sender == self.ui.motor_forward:
                dir = "f"
                vol = "{:0>2d}".format(int(self.ui.forward_vol.currentText()[:-1]))
            elif sender == self.ui.motor_backward:
                dir = "b"
                vol = "{:0>2d}".format(int(self.ui.backward_vol.currentText()[:-1]))

            str2send = dir + vol + "\r\n"
            gl.mainserial.write(str2send.encode("gbk"))

    def motor_stop(self):
        self.time.stop()
        self.count = 0
        if self.port_state:
            gl.mainserial.write("s00\r\n".encode("gbk"))

    def time_refresh(self):
        self.count += 1
        if self.ui.motor_forward.isDown():
            self.ui.forward_time.setText("%.1fs"%(0.1*self.count))
        elif self.ui.motor_backward.isDown():
            self.ui.backward_time.setText("%.1fs" % (0.1 * self.count))


if __name__ == "__main__":

    #高分辨率自适应，解决运行与preview效果不一致的问题
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    #--------------

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = motorui.Ui_MainWindow()
    ui.setupUi(mainWindow)
    binding = Binding(ui, mainWindow)

    binding.re_serial_port(0)

    mainWindow.show()
    sys.exit(app.exec_())
