import serial #导入模块
import threading
import serial.tools.list_ports
from queue import Queue
import time
from mycode import globalvar as gl
from PyQt5.QtGui import QTextCursor
from winreg import OpenKey, HKEY_LOCAL_MACHINE, EnumValue

def scan_serialport():
    key = OpenKey(HKEY_LOCAL_MACHINE, r"HARDWARE\\DEVICEMAP\\SERIALCOMM")
    gl.port_list.clear()
    try:
        i=0
        while 1:
            name, value, type = EnumValue(key, i)
            gl.port_list.append(value + " - " + name)
            i+=1
    except FileNotFoundError:
        print("FileNotFound when scanning COM")
    except OSError:
        pass


class Myserial(serial.Serial):

    def __init__(self, *args, **kwargs):  #创建串口对象，初始化变量

        #从kwarg字典中删除timeinterval，否则调用super时会因多余的关键字参数出错
        try:
            self.timeinterval = kwargs.pop("timeinterval")
        except KeyError:
            self.timeinterval = 0.2  #默认值
        try:
            self.textbox = kwargs.pop("textbox")
        except KeyError:
            self.textbox = 0
        try:
            self.queue = kwargs.pop("queue")
        except KeyError:
            self.queue = []
        #----------------------------------------------------------

        super(Myserial,self).__init__(*args, **kwargs)
        self.read_enable = 0
        self.history = ""
        self.thread = threading.Thread(target = self.read_loop)    #为循环读取创建线程
        self.thread.setDaemon(True)
    #==================================================

    def read_loop(self): #循环读取串口输入，放入queue，更新串口显示窗口
        while self.read_enable:                                             #使能flag
            
            if self.in_waiting:
                self.newcontent = self.read(self.in_waiting).decode("gbk")  #读取新内容

                self.history += self.newcontent                           #将新内容加入历史内容
                self.queue.put(self.newcontent)                             #新内容加入队列

                if self.textbox:
                    self.textbox.put(self.newcontent)



                if __name__ == "__main__":                                   #测试，打印
                    print(self.newcontent)

            time.sleep(self.timeinterval)
    #=======================================================


    def start_loop(self):   #开始读取
        if self.in_waiting:
            self.read(self.in_waiting)  # 开始读取之前把串口积攒的数据读掉
        self.read_enable = 1                                       #使能flag
        self.thread = threading.Thread(target=self.read_loop)  # 为循环读取创建线程
        self.thread.setDaemon(True)
        self.thread.start()  # 开启线程
    #=============================================

    def stop_loop(self):
        self.read_enable = 0
        self.thread.join()  # 合并线程
    #=============================================
        

    def close(self):     #停止读取串口、结束读取进程、关闭串口
        try:
            self.stop_loop()
        except:
            pass
        serial.Serial.close(self)
    #=================================

    def clear(self):
        self.history = ""
        self.newcontent = ""
    #================================
#==============================================



if __name__=="__main__":
    
    testserial = Myserial("COM1", 9600, timeout = None)
    if testserial.is_open:
        print("串口已打开")
        testserial.write("串口打开成功\n".encode("gbk"))
        testserial.start_loop()
        print("此时循环接收数据，20秒后结束")

        time.sleep(20)
        print("结束")
        testserial.close()
        print("关闭串口")
        print("20秒后退出程序，此时串口应已断开")
        time.sleep(20)

