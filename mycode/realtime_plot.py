from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import Queue



class RtPlot:

	def __init__(self,master,queue = [],interval = 0.2):
		self.interval = interval
		self.master = master
		self.queue = queue
		self.fig = plt.figure()  #创建画布


		if __name__ == '__main__':
			self.ax0 = self.fig.add_subplot(221)
			self.ax0_ln1_data = {'x':[], 'y':[]}
			self.ax0_ln2_data = {'x':[], 'y':[]}
			self.ax0_ln1, = self.ax0.plot(self.ax0_ln1_data['x'],self.ax0_ln1_data['y'],label = 'square')
			self.ax0_ln2, = self.ax0.plot(self.ax0_ln2_data['x'],self.ax0_ln2_data['y'], label = 'cube')
			self.ax0.grid()
			# ax.set_ylabel("distance")
			self.ax0.legend()
			# 设置坐标轴刻度
		    # my_y_ticks1 = np.arange(-4, 4, 1)
		    # plt.yticks(my_y_ticks1)
		else:
			#数据
			self.time = []
			self.temperature = []
			self.distance = []
			self.force = []

			#温度曲线
			self.temperature_ax = self.fig.add_subplot(221)
			self.temperature_ln, = self.temperature_ax.plot(self.time,self.temperature,label = 'temperature')
			self.temperature_ax.grid()

			#位移曲线
			self.distance_ax = self.fig.add_subplot(222)
			self.distance_ln, = self.distance_ax.plot(self.time,self.distance,label = 'distance')
			self.distance_ax.grid()

			#力曲线
			self.force_ax = self.fig.add_subplot(223)
			self.force_ln, = self.force_ax.plot(self.time,self.force,label = 'force')
			self.force_ax.grid()

			#对应曲线
			self.fuse_ax = self.fig.add_subplot(224)
			self.fuse_ln, = self.fuse_ax.plot([],[])
			self.fuse_ax.grid()
		#--------------------------------------------------

		self.canvas = FigureCanvasTkAgg(self.fig, master = master) #生成画布控件
		self.canvas.draw()	    # 显示画布控件
		self.canvas.get_tk_widget().pack()   #打包，显示在tkinter上

		toolbar = NavigationToolbar2Tk(self.canvas, master)
		toolbar.update()
		self.canvas.get_tk_widget().pack()

	def update(self,gen):
		if __name__ == '__main__': #测试
			i = gen
			self.ax0_ln1_data['x'].append(i)
			self.ax0_ln1_data['y'].append(i*2)
			self.ax0_ln2_data['x'].append(i)
			self.ax0_ln2_data['y'].append(i*3)

			self.ax0_ln1.set_data(self.ax0_ln1_data['x'],self.ax0_ln1_data['y'])
			self.ax0_ln2.set_data(self.ax0_ln2_data['x'],self.ax0_ln2_data['y'])

			self.ax0.set_xlim(0,max(self.ax0_ln1_data['x'])/0.9)
			self.ax0.set_ylim(0,max(self.ax0_ln2_data['y'])/0.9)
		else:                     #嵌入运行
			if gen:
				for eachline in gen:
					list = gen.split(',')
					if len(list) == 4:
						try:
							self.time.append(float(list[0]))
							self.temperature.append(float(list[1]))
							self.distance.append(float(list[2]))
							self.force.append(float(list[3]))
						except ValueError:
							pass

				self.temperature_ln.set_data(self.time,self.temperature)
				self.distance_ln.set_data(self.time,self.distance)
				self.force_ln.set_data(self.time,self.force)
				self.fuse_ln.set_data(self.temperature,self.force)

				if self.time:
					maxtime = max(self.time)/0.9
					self.temperature_ax.set_xlim(0,maxtime)
					self.distance_ax.set_xlim(0,maxtime)
					self.force_ax.set_xlim(0,maxtime)
				if self.temperature:
					self.temperature_ax.set_ylim(min(self.temperature)/0.9,max(self.temperature)/0.9)
				if self.distance:
					self.distance_ax.set_ylim(min(self.distance)/0.9,max(self.distance)/0.9)
				if self.force:
					self.force_ax.set_ylim(min(self.force)/0.9,max(self.force)/0.9)
				'''
				self.fuse_ax.set_xlim(self.temperature.ylim())
				self.fuse_ax.set_ylim(self.distance.ylim())
				'''


	def genfunc(self):
		if __name__ == '__main__':
			i = 0
			while 1:
				i += 1
				yield i
		else:
			while 1:
				if not (self.queue.empty()):
					gen = self.queue.get()
					yield gen
				else:
					yield ""

	def initfunc(self):
		pass

	def start(self):
		self.ani = FuncAnimation(self.fig, self.update, frames=self.genfunc,init_func=self.initfunc, blit=False)
		self.canvas.draw()

	def stop(self):
		self.ani.event_source.stop()

	def resume(self):
		self.ani.event_source.start()

	def clear(self):
		if __name__ == '__main__':
			self.ax0_ln1_data['x'].clear()
			self.ax0_ln1_data['y'].clear()
			self.ax0_ln2_data['x'].clear()
			self.ax0_ln2_data['y'].clear()
		else:
			self.time.clear()
			self.temperature.clear()
			self.distance.clear()
			self.force.clear()
			self.queue.queue.clear()


	def force_draw(self):
		self.ani._step()


if __name__ == '__main__':
	from tkinter import *
	import threading
	import time

	def stop(n):
		i = 0
		while 1:
			i+= 1
			time.sleep(1)
			n.stop()
			time.sleep(1)
			n.resume()

			if i%3 == 0:
				n.stop()
				n.clear()
				n.force_draw()
			


	root = Tk()
	rtplot = RtPlot(root)
	rtplot.start()

	newthread = threading.Thread(target = stop, args = ([rtplot]))
	newthread.start()

	root.mainloop()
	newthread.join()
	
