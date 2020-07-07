# -*- coding: utf-8 -*-
# Author：Tang XT
# Time: 2020/6/30/18:58
# File name：myQtGraph.py

import pyqtgraph as pg
from queue import Queue
from PyQt5.QtWidgets import QGridLayout, QWidget, QApplication
from PyQt5 import QtCore
from PyQt5 import QtGui
import bisect
#import numpy as np


class MyQtGraph():

    def __init__(self, queue, mode):
        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        # pg.setConfigOption('background', 'w')
        # pg.setConfigOption('foreground', 'k')


        self.temperaturePlot = pg.PlotWidget(title="Temperature")
        self.forcePlot = pg.PlotWidget(title="Force")
        self.positionPlot = pg.PlotWidget(title="Position")
        self.versus = pg.PlotWidget(title="Versus")

        font = QtGui.QFont()
        font.setPixelSize(20)


        listtemp = [self.temperaturePlot, self.forcePlot, self.positionPlot]
        for each in listtemp:
            each.showGrid(x=True, y=True, alpha=0.5)
            each.setLabel('bottom', "Time", units='s')
            each.getAxis("bottom").tickFont = font
        del(listtemp)
        self.temp_curve_0 = self.temperaturePlot.plot()
        self.temp_curve_1 = self.temperaturePlot.plot()
        self.temp_curve_2 = self.temperaturePlot.plot()
        self.temp_curve_3 = self.temperaturePlot.plot()

        self.force_curve_1 = self.forcePlot.plot()
        self.pos_curve_1 = self.positionPlot.plot()
        self.versue_curve_1 = self.versus.plot()

        self.flag = 0
        self.queue = queue
        self.mode = mode

        self.time_list = [0]
        self.temp0Tar_list = [0]
        self.temp0_list = [0]
        self.temp1Tar_list = [0]
        self.temp1_list = [0]
        self.force_list = [0]
        self.position_list = [0]
        self.data = [self.time_list,self.temp0Tar_list, self.temp0_list,self.temp1Tar_list, self.temp1_list]
        self.half_line = ""

        self.grid.addWidget(self.temperaturePlot,0,0)
        self.grid.addWidget(self.forcePlot, 0, 1)
        self.grid.addWidget(self.positionPlot,1,0)
        self.grid.addWidget(self.versus, 1, 1)

        self.time = QtCore.QTimer()
        self.time.setInterval(50)  #16ms 60fps
        self.time.timeout.connect(self.update)

        self.templabel = pg.TextItem()
        self.temperaturePlot.addItem(self.templabel,ignoreBounds=True)
        self.tempvLine = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.temphLine = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.temperaturePlot.addItem(self.tempvLine, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.temperaturePlot.addItem(self.temphLine, ignoreBounds=True)  # 在图形部件中添加水平线条

        self.move_slot = pg.SignalProxy(self.temperaturePlot.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_move)

    def mouse_move(self,event = None):
        if event is None:
            print("事件为空")
        else:
            pos = event[0]  # 获取事件的鼠标位置
            try:
                # 如果鼠标位置在绘图部件中
                if self.temperaturePlot.sceneBoundingRect().contains(pos):
                    mousePoint = self.temperaturePlot.plotItem.vb.mapSceneToView(pos)  # 转换鼠标坐标

                    index = bisect.bisect(self.time_list,mousePoint.x())  # 鼠标所处的X轴坐标
                    #print(index)

                    pos_y = int(mousePoint.y())  # 鼠标所处的Y轴坐标
                    if 0 < index < len(self.time_list):
                        #在label中写入HTML
                        self.templabel.setHtml(
                            "<p style='color:white'><strong>时间：{0}</strong></p><p style='color:white'>温度：{1}</p><p".format(
                                self.time_list[index], self.temp0_list[index]))

                self.templabel.setPos(mousePoint.x(), mousePoint.y())  # 设置label的位置
                self.tempvLine.setPos(mousePoint.x())
                self.temphLine.setPos(mousePoint.y())
            except Exception as e:
                #print(e)
                pass
                #print(traceback.print_exc())

    def decode(self):
        new_text = ""
        while not (self.queue.empty()):
            new_text += self.queue.get()  # queue中的新文本读进来
        new_text = self.half_line + new_text  # 跟之前剩下的半行合并

        lines = new_text.split("\n")[:-1]  # 整个文本分割成行
        self.half_line = new_text.split("\n")[-1]


        for each_line in lines:
            data = each_line.split(",")  # 每行文本用逗号分割
            data_copy = []

            for each in data:
                if each =='inf' or each == 'nan':
                    each = 22
                try:
                    data_copy.append(float(each))
                except:
                    data_copy.append(0)
                    continue
                    #break
            else:
                try:

                    self.time_list.append(float(data_copy[0]))
                    self.temp0Tar_list.append(float(data_copy[1]))
                    self.temp1Tar_list.append(float(data_copy[2]))
                    self.temp0_list.append(float(data_copy[3]))
                    self.temp1_list.append(float(data_copy[4]))

                    #print(data[0])
                    #print(len(self.time_list),len(self.temperature_list),len(self.force_list),len(self.position_list))
                except Exception as e:
                    self.clear()
                    print("cleared when decode")
                    print(e)
            continue
    # ===================================

    def update(self):

        self.decode()
        try:
            self.temp_curve_0.setData(self.time_list,self.temp0Tar_list)
            self.temp_curve_1.setData(self.time_list, self.temp1Tar_list)
            self.temp_curve_2.setData(self.time_list, self.temp0_list)
            self.temp_curve_3.setData(self.time_list, self.temp1_list)
            print(self.temp0_list)


        except Exception as e:
            self.clear()
            print("cleared when update")
            print(e)

    #=========================



    def start_plot(self):
        self.clear()
        self.time.start()
    #=================
    def stop_plot(self):
        self.time.stop()
    #==========

    def clear(self):
        for each in self.data:
            each.clear()
        #self.half_line = ""
        self.update()
    #=========================
#=======================

if __name__ == "__main__":
    import time
    import threading
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    queue1 = Queue()
    app = QApplication(sys.argv)
    testwindow = QWidget()
    testgraph = MyQtGraph(queue1,1)
    testwindow.setLayout(testgraph.grid)
    testwindow.show()
    #testgraph.start_plot()
    count = 0
    testgraph.start_plot()


    def gen():
        count = 0
        while 1:
            count+=1
            text = "{0},{1},{2},{3},{4}\r\n".format(count,2*count,3*count,4*count,5*count)
            queue1.put(text)
            time.sleep(0.1)
            #print(text)

    thread1 = threading.Thread(target = gen)
    thread1.start()


    sys.exit(app.exec_())


