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
        self.graph = MyQtGraph(gl.queue1,0)
        self.ui.groupBox_graph.setLayout(self.graph.grid)

        #初始设成第一个选项卡
        self.ui.tabWid.setCurrentIndex(0)

        #mode选择
        self.ui.mode_select.setCurrentIndex(0)
        self.ui.mode_select.activated.connect(self.changeMode)
        self.changeMode(0)

        #start,ctrl按钮，按钮可选择
        self.ui.startSample.clicked.connect(self.start_clicked)
        self.ui.startSample.setCheckable(True)
        self.ui.ctrlStart.setCheckable(True)
        self.ui.ctrlStart.clicked.connect(self.ctrl_clicked)

        #cali 按钮
        self.ui.t_cali.clicked.connect(self.t_cali_clicked)
        self.ui.f_cali.clicked.connect(self.f_cali_clicked)
        self.ui.p_cali.clicked.connect(self.p_cali_clicked)
        self.sys_flag = '0'

        #clear, send, save 按钮
        self.ui.save.clicked.connect(self.save_data)
        self.ui.clear.clicked.connect(self.clear_clicked)
        self.ui.send.clicked.connect(self.send)


        #lineEdit赋初值
        self.ui.lineEdit_SamplePeriod.setText("10")
        self.ui.lineEdit_F_SetPoint.setText("0")
        self.ui.lineEdit_T_SetPoint.setText("0")
        self.ui.lineEdit_P_SetPoint.setText("0")
        self.ui.lineEdit_T_Kp.setText("1.2")
        self.ui.lineEdit_T_Ti.setText("1")
        self.ui.lineEdit_T_Td.setText("0")
        self.ui.lineEdit_F_Kp.setText("0")
        self.ui.lineEdit_F_Ti.setText("0")
        self.ui.lineEdit_F_Td.setText("0")
        self.ui.lineEdit_P_Kp.setText("0")
        self.ui.lineEdit_P_Ti.setText("0")
        self.ui.lineEdit_P_Td.setText("0")
        self.ui.lineEdit_Scan_Period.setText("0")

        #初始化定时器，用来触发面板更新
        self.textTime = QtCore.QTimer()
        self.textTime.setInterval(500)
        self.textTime.timeout.connect(self.update_panel)

    #模式变化
    def changeMode(self, index):
        self.graph.mode = index

    #串口选择下拉菜单被激活
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
    #打开串口
    def openSerial(self):
        if self.ui.open_serial.isChecked():

            self.ui.open_serial.setChecked(False)
            gl.mainserial = Myserial(self.ui.port_select.currentText().split(" ")[0], \
                                         int(self.ui.baund_rate.currentText()), timeout=None, textbox=gl.textQueue, queue=gl.queue1, timeinterval=0.05, rtscts=True,dsrdtr=True)

            try:
                self.port_state = gl.mainserial.is_open
            except:
                self.port_state = 0
            if self.port_state:
                self.ui.open_serial.setText("关闭\n串口")
                self.ui.open_serial.setChecked(True)
                gl.mainserial.start_loop()
                self.textTime.start()

        else:
            self.ui.open_serial.setChecked(True)
            gl.mainserial.close()
            self.textTime.stop()
            try:
                self.port_state = gl.mainserial.is_open
            except:
                self.port_state = 0

            if not self.port_state:
                self.ui.open_serial.setText("打开\n串口")
                self.ui.open_serial.setChecked(False)

    #采样按钮按下，发送指令，绘图启停
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

    #控制按钮按下
    def ctrl_clicked(self):
        self.send()

    #clear按下
    def clear_clicked(self):
        self.graph.clear()
        gl.mainserial.clear()
        self.ui.textBrowser_RecText.clear()

    #send按下
    def send(self):
        try:
            samplePeriod = int(self.ui.lineEdit_SamplePeriod.text())
            mode = int(str(self.ui.mode_select.currentIndex()))
            scanEnable = int(self.ui.scanEnable.isChecked())
            scanPeriod = int(self.ui.lineEdit_Scan_Period.text())
            fSetPoint = int(self.ui.lineEdit_F_SetPoint.text())
            tSetPoint = int(self.ui.lineEdit_T_SetPoint.text())
            pSetPoint = int(self.ui.lineEdit_P_SetPoint.text())
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
            send_content = "{sys_flag}{start_flag:1d}{ctrl_flag:1d}{mode:1d}{scanEnable:1d}{samplePeriod:03d}{scanPeriod:03d}{tSetPoint:03d}{fSetPoint:03d}{pSetPoint:03d}{t_Kp:03d}{t_Ti:03d}{t_Td:03d}{f_Kp:03d}{f_Ti:03d}{f_Td:03d}{p_Kp:03d}{p_Ti:03d}{p_Td:03d}".format(samplePeriod=samplePeriod,\
                 tSetPoint=tSetPoint,pSetPoint=pSetPoint,fSetPoint=fSetPoint, start_flag=start_flag, ctrl_flag=ctrl_flag,\
                t_Kp=t_Kp, t_Ti=t_Ti, t_Td=t_Td,sys_flag = self.sys_flag, mode=mode, scanEnable=scanEnable, scanPeriod=scanPeriod,\
                 f_Kp=f_Kp, f_Ti=f_Ti, f_Td=f_Td, p_Kp=p_Kp, p_Ti=p_Ti, p_Td=p_Td)
            print(send_content)
            self.ui.textBrowser_SentText.setText(send_content)
            gl.mainserial.write((send_content+"\r\n").encode())
        except:
            self.ui.textBrowser_SentText.setText("send Error")

    #t_cali按下
    def t_cali_clicked(self):
        self.sys_flag = 'T'
        self.send()
        self.sys_flag = '0'

    #f_cali按下
    def f_cali_clicked(self):
        self.sys_flag = 'F'
        self.send()
        self.sys_flag = '0'

    def p_cali_clicked(self):
        self.sys_flag = 'P'
        self.send()
        self.sys_flag = '0'

    #保存文件
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

    #更新面板数值显示
    def update_panel(self):
        new_text = ""
        while not (gl.textQueue.empty()):
            new_text = gl.textQueue.get()  # queue中的新文本读进来
            self.ui.textBrowser_RecText.moveCursor(QTextCursor.End)
            self.ui.textBrowser_RecText.insertPlainText(new_text)
            self.ui.temp_real.setText(str(self.graph.temp_list[-1]))
            self.ui.force_real.setText(str(self.graph.force_list[-1]))
            self.ui.dis_real.setText(str(self.graph.pos_list[-1]))


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
