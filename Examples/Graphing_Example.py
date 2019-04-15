#import serial
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


root = Tk()
root.geometry('1200x700+200+100')
root.title('This is my root window')
root.config(background='#fafafa')


xar = []
insideTemp = []
xar2 = []
outsideTemp = []
xar3 = []
row1 = []
xar4 = []
row2 = []
xar5 = []
row3 = []

def addPoint():
    data = random.sample(range(0, 100),1)
    return data

def addRow1Data():
    data = addPoint()
    row1.append(data)
    return row1

def addRow2Data():
    data = addPoint()
    row2.append(data)
    return row2

def addRow3Data():
    data = addPoint()
    row1.append(data)
    return row3

def addInTempData():
    data = addPoint()
    insideTemp.append(data)
    return insideTemp

def addOutTempData():
    data = addPoint()
    outsideTemp.append(data)
    return outsideTemp



def animate(i):
    addRow1Data()
    addRow2Data()
    addRow3Data()
    addInTempData()
    addOutTempData()
    
    iT = insideTemp[-10:]
    oT= outsideTemp[-10:]
    R1 = row1[-10:]
    R2 = row2[-10:]
    R3 = row3[-10:]
    line1.set_data(xar, iT)
    line2.set_data(xar2, oT)
    line3.set_data(xar3, R1)
    line4.set_data(xar4, R2)
    line5.set_data(xar5, R3)
    
    ax1.set_xlim(0, 10)
    ax2.set_xlim(0, 10)

style.use('ggplot')
fig = plt.figure(figsize=(10, 3), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim(0, 150)
line1, line2 = ax1.plot(xar, insideTemp, '--o', xar2, outsideTemp, '--bo')
ax1.set_title('Temperature', fontsize=16)
ax1.legend((line1,line2), ('Temp Inside','Temp Outside'), loc='upper right', shadow=True)


fig2 = plt.figure(figsize=(10, 3), dpi=100)
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_ylim(0, 150)
line3, line4, line5 = ax2.plot(xar3, row1, '--ro', xar4, row2, '--go', xar5, row3, '--yo')
ax2.set_title('Moisture', fontsize=16)
ax2.legend((line3,line4,line5), ('Row 1','Row 2','Row 3'), loc='upper right', shadow=True)
plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().grid(column=1, row=1)
plotcanvas2 = FigureCanvasTkAgg(fig2, root)
plotcanvas2.get_tk_widget().grid(column=1, row=3)
    
ani2 = animation.FuncAnimation(fig, animate, interval=3000, blit=False)
ani2 = animation.FuncAnimation(fig2, animate, interval=3000, blit=False)

root.mainloop()
