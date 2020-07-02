# -*- coding: utf-8 -*-
# Author：Tang XT
# Time: 2020/5/21/21:17
# File name：runmainwindow.py

import sys
import motorui
from mycode import globalvar as gl
from mycode.myserial import *
from mycode.myQtGraph import *
import threading
import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QWidget, QAction, QGridLayout, QFileDialog, QMessageBox
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
        self.re_serial_port(0)
        #------

        #波特率选择栏
        self.ui.baund_rate.setCurrentIndex(-1)
        #-------

        #打开串口按钮
        self.ui.open_serial.clicked.connect(self.openSerial)
        self.ui.open_serial.setCheckable(True)
        #---------

        #初始化绘图
        self.graph = MyQtGraph(gl.queue1,'1')
        self.ui.groupBox_graph.setLayout(self.graph.grid)

        #初始设成第一个选项卡
        self.ui.tabWid.setCurrentIndex(0)

        #mode选择
        self.ui.mode_select.setCurrentIndex(0)
        self.ui.mode_select.activated.connect(self.changeMode)
        self.changeMode(0)

        self.ui.startSample.clicked.connect(self.start_clicked)
        self.ui.startSample.setCheckable(True)

        self.ui.save.clicked.connect(self.save_data)
        self.ui.clear.clicked.connect(self.clear_clicked)
        self.ui.send.clicked.connect(self.send)

        self.ui.ctrlStart.setCheckable(True)
        self.ui.ctrlStart.clicked.connect(self.ctrl_clicked)

        self.ui.lineEdit_SamplePeriod.setText("50")
        self.ui.lineEdit_F_SetPoint.setText("0")
        self.ui.lineEdit_P_SetPoint.setText("0")
        self.ui.lineEdit_T_SetPoint.setText("0")
        self.ui.lineEdit_T_Kp.setText("0")
        self.ui.lineEdit_T_Ti.setText("0")
        self.ui.lineEdit_T_Td.setText("0")
        self.ui.lineEdit_F_Kp.setText("0")
        self.ui.lineEdit_F_Ti.setText("0")
        self.ui.lineEdit_F_Td.setText("0")
        self.ui.lineEdit_P_Kp.setText("0")
        self.ui.lineEdit_P_Ti.setText("0")
        self.ui.lineEdit_P_Td.setText("0")
        self.ui.lineEdit_Scan_Period.setText("0")

    def changeMode(self, index):
        if index == 0:
            self.ui.lineEdit_F_SetPoint.setEnabled(True)
            self.ui.lineEdit_P_SetPoint.setEnabled(False)
            self.ui.lineEdit_T_SetPoint.setEnabled(True)
        elif index == 1:
            self.ui.lineEdit_F_SetPoint.setEnabled(True)
            self.ui.lineEdit_P_SetPoint.setEnabled(False)
            self.ui.lineEdit_T_SetPoint.setEnabled(True)
        elif index == 2:
            self.ui.lineEdit_F_SetPoint.setEnabled(False)
            self.ui.lineEdit_P_SetPoint.setEnabled(True)
            self.ui.lineEdit_T_SetPoint.setEnabled(True)

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
            setPortlist()
            # newthread = threading.Thread(target= setPortlist)
            # newthread.start()

    def openSerial(self):
        if self.ui.open_serial.isChecked():

            self.ui.open_serial.setChecked(False)
            gl.mainserial = Myserial(self.ui.port_select.currentText().split(" ")[0], \
                                         int(self.ui.baund_rate.currentText()), timeout=None, textbox=self.ui.textBrowser_RecText, queue=gl.queue1, rtscts=True,dsrdtr=True)

            try:
                self.port_state = gl.mainserial.is_open
            except:
                self.port_state = 0
            if self.port_state:
                self.ui.open_serial.setText("关闭\n串口")
                self.ui.open_serial.setChecked(True)
                gl.mainserial.start_loop()

        else:
            self.ui.open_serial.setChecked(True)
            gl.mainserial.close()
            try:
                self.port_state = gl.mainserial.is_open
            except:
                self.port_state = 0

            if not self.port_state:
                self.ui.open_serial.setText("打开\n串口")
                self.ui.open_serial.setChecked(False)

    def start_clicked(self):
        if self.ui.startSample.isChecked():
            print("采样键按下")
            self.graph.start_plot()
            self.ui.startSample.setText("Stop")
        else:
            #gl.mainserial.stop_loop()
            self.graph.stop_plot()
            self.ui.startSample.setText("Start")
            print("采样停止按下")
        self.send()

    def ctrl_clicked(self):
        self.send()


    def clear_clicked(self):
        self.graph.clear()
        gl.mainserial.clear()
        self.ui.textBrowser_RecText.clear()

    def send(self):
        try:
            samplePeriod = int(self.ui.lineEdit_SamplePeriod.text())
            mode = int(str(self.ui.mode_select.currentIndex()))
            scanEnable = int(self.ui.scanEnable.isChecked())
            scanPeriod = int(self.ui.lineEdit_Scan_Period.text())
            fSetPoint = int(self.ui.lineEdit_F_SetPoint.text())
            pSetPoint = int(10*float(self.ui.lineEdit_P_SetPoint.text()))
            tSetPoint = int(self.ui.lineEdit_T_SetPoint.text())
            start_flag = int(self.ui.startSample.isChecked())
            ctrl_flag = int(self.ui.ctrlStart.isChecked())
            t_Kp = int(10*float(self.ui.lineEdit_T_Kp.text()))
            t_Ti = int(10*float(self.ui.lineEdit_T_Ti.text()))
            t_Td = int(100*float(self.ui.lineEdit_T_Td.text()))
            f_Kp = int(10*float(self.ui.lineEdit_F_Kp.text()))
            f_Ti = int(10*float(self.ui.lineEdit_F_Ti.text()))
            f_Td = int(100*float(self.ui.lineEdit_F_Td.text()))
            p_Kp = int(10*float(self.ui.lineEdit_P_Kp.text()))
            p_Ti = int(10*float(self.ui.lineEdit_P_Ti.text()))
            p_Td = int(100*float(self.ui.lineEdit_P_Td.text()))
            send_content = "{samplePeriod:02d}{mode:1d}{scanEnable:1d}{scanPeriod:02d}{fSetPoint:05d}{pSetPoint:04d}{tSetPoint:03d}{start_flag:1d}{ctrl_flag:1d}{t_Kp:03d}{t_Ti:03d}{t_Td:03d}{f_Kp:03d}{f_Ti:03d}{f_Td:03d}{p_Kp:03d}{p_Ti:03d}{p_Td:03d}".format(samplePeriod=samplePeriod,
                mode=mode, scanEnable=scanEnable, fSetPoint=fSetPoint,\
                pSetPoint=pSetPoint, tSetPoint=tSetPoint, start_flag=start_flag, ctrl_flag=ctrl_flag,\
                t_Kp=t_Kp, t_Ti=t_Ti, t_Td=t_Td, f_Kp=f_Kp, f_Ti=f_Ti, f_Td=f_Td, p_Kp=p_Kp, p_Ti=p_Ti, p_Td=p_Td, scanPeriod = scanPeriod)
            print(send_content)
            self.ui.textBrowser_SentText.setText(send_content)
            gl.mainserial.write((send_content+"\r\n").encode())
        except:
            self.ui.textBrowser_SentText.setText("send Error")




    def save_data(self):
        def saveFile():
            # get_directory_path = QFileDialog.getExistingDirectory(self,
            #                                                       "选取指定文件夹",
            #                                                       "C:/")
            # self.filePathlineEdit.setText(str(get_directory_path))

            get_filename_path, ok = QFileDialog.getSaveFileName(self,
                                                                "选取单个文件",
                                                                os.getcwd(),
                                                                "Text Files (*.txt);;All Files (*)")
            if ok:
                fileName=(str(get_filename_path))
                print(fileName)

            try:
                with open (fileName, 'w') as f:
                    text = gl.mainserial.history
                    f.write(text)
            except AttributeError:
                QMessageBox.warning(self,"warning","反正是有个错误",QMessageBox.Ok,QMessageBox.Ok)

            # get_filenames_path, ok = QFileDialog.getOpenFileNames(self,
            #                                                       "选取多个文件",
            #                                                       "C:/",
            #                                                       "All Files (*);;Text Files (*.txt)")
            # if ok:
            #     self.filePathlineEdit.setText(str(' '.join(get_filenames_path)))
        saveFile()

    def update_panel(self):
        pass


    #
    # def motor_move(self):
    #     self.time.start()
    #     if self.port_state:
    #         sender = self.mainwindow.sender()
    #         if sender == self.ui.motor_forward:
    #             dir = "f"
    #             vol = "{:0>2d}".format(int(self.ui.forward_vol.currentText()[:-1]))
    #         elif sender == self.ui.motor_backward:
    #             dir = "b"
    #             vol = "{:0>2d}".format(int(self.ui.backward_vol.currentText()[:-1]))
    #
    #         str2send = dir + vol + "\r\n"
    #         gl.mainserial.write(str2send.encode("gbk"))
    #
    # def motor_stop(self):
    #     self.time.stop()
    #     self.count = 0
    #     if self.port_state:
    #         gl.mainserial.write("s00\r\n".encode("gbk"))
    #
    # def time_refresh(self):
    #     self.count += 1
    #     if self.ui.motor_forward.isDown():
    #         self.ui.forward_time.setText("%.1fs"%(0.1*self.count))
    #     elif self.ui.motor_backward.isDown():
    #         self.ui.backward_time.setText("%.1fs" % (0.1 * self.count))
    #
    # def openFile(self):
    #     # get_directory_path = QFileDialog.getExistingDirectory(self,
    #     #                                                       "选取指定文件夹",
    #     #                                                       "C:/")
    #     # self.filePathlineEdit.setText(str(get_directory_path))
    #
    #     get_filename_path, ok = QFileDialog.getOpenFileName(self,
    #                                                         "选取单个文件",
    #                                                         "C:/",
    #                                                         "All Files (*);;Text Files (*.txt)")
    #     if ok:
    #         self.filePathlineEdit.setText(str(get_filename_path))
    #
    #     get_filenames_path, ok = QFileDialog.getOpenFileNames(self,
    #                                                           "选取多个文件",
    #                                                           "C:/",
    #                                                           "All Files (*);;Text Files (*.txt)")
    #     if ok:
    #         self.filePathlineEdit.setText(str(' '.join(get_filenames_path)))


if __name__ == "__main__":

    #高分辨率自适应，解决运行与preview效果不一致的问题
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    #--------------

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = motorui.Ui_MainWindow()
    ui.setupUi(mainWindow)
    binding = Binding(ui, mainWindow)

    #binding.re_serial_port(0)

    mainWindow.show()
    sys.exit(app.exec_())
