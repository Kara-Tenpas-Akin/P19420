#import serial
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = Tk()
root.geometry('1200x700+200+100')
root.title('This is my root window')
root.config(background='#fafafa')

style.use('ggplot')
fig = plt.figure(figsize=(10, 3), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim(0, 150)
#line1, line2 = ax1.plot(xar, yar, '--o', xar2, yar2, '--bo')
ax1.set_title('Temperature', fontsize=16)
ax1.legend((line1,line2), ('Temp Inside','Temp Outside'), loc='upper right', shadow=True)

plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().grid(column=1, row=1)

fig2 = plt.figure(figsize=(10, 3), dpi=100)
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_ylim(0, 150)
#line3, line4, line5 = ax2.plot(xar3, yar3, '--ro', xar4, yar4, '--go', xar5, yar5, '--yo')
ax2.set_title('Moisture', fontsize=16)
ax2.legend((line3,line4,line5), ('Row 1','Row 2','Row 3'), loc='upper right', shadow=True)

plotcanvas2 = FigureCanvasTkAgg(fig2, root)
plotcanvas2.get_tk_widget().grid(column=1, row=3) 

xar = [0] * 10
yar = [0] * 10
yar2 = [0] * 10
yar3 = [0] * 10
yar4 = [0] * 10
yar5 = [0] * 10

def animate(i):
    xar.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    yar.append(99-i)
    yar2.append(88-i)
    yar3.append(99-i)
    yar4.append(88-i)
    yar5.append(77-i)

    xar = xar[-10:]
    yar = yar[-10:]
    yar2 = yar[-10:]
    yar3 = yar[-10:]
    yar4 = yar[-10:]
    yar5 = yar[-10:]

    ax1.clear()
    ax2.clear()

    ax1.plot(xar,yar, xar, yar2)
    ax2.plot(xar, yar3, xar)

ani = animation.FuncAnimation(fig, animate, interval=800, blit=False)
ani2 = animation.FuncAnimation(fig2, animate, interval=1000, blit=False)

root.mainloop()
