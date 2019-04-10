#!/usr/bin/env python3
# Graphical User Interface for RIT MSD P19420
# Created by Kara Tenpas-Akin
from tkinter import *           # The Tk package
from tkinter import ttk
from tkinter import messagebox
from Communication import commThread2 as comm
import tkinter as tk
import Pmw                   # The Python MegaWidget package
import datetime as dt
import math, threading, time, random
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class guiThread1(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        print("Comm thread is initialized")
    
    # Functions
    def client_exit(self):
        #queue.put("e")
        exit()
    
    def download(self):
        messagebox.showinfo('Download Data', 'Download completed.')
    
    def refresh(self):
        messagebox.showinfo('Refresh', 'Refresh of graphs completed.')
    
    def fertigate(self):
        MsgBoxF = messagebox.askyesnocancel('Fetigation System', 'Turn on fertigation system?')
        if MsgBoxF == "Yes":
            print('yes')
        if MsgBoxF == "No":
            print('no')
    
    def water(self):
        messagebox.askyesnocancel('Irrigation System', 'Turn on irragation system?')
    
    def heat(self):
        messagebox.askyesnocancel('Heating System', 'Turn on heating system?')

    def run(self):
        while(True):

            root = Tk()
            root.title('Blackberry High Tunnel')
            
            # Creation of Tabs
            tab_control = ttk.Notebook(root)
            tab1 = ttk.Frame(tab_control)
            tab2 = ttk.Frame(tab_control)
            tab3 = ttk.Frame(tab_control)
            tab4 = ttk.Frame(tab_control)
            
            # Tab 1
            tab_control.add(tab1, text='Status')
            # Buttons
            quitButton = Button(tab1, text="Emergency Stop", command=self.client_exit, bg="red", fg="white", height = 5, width = 20)
            quitButton.grid(row=0, column=2)
            # Text
            Title = Label(tab1, text="Durgin Family Farms Blackberry Hightunnel", font=("Helvetica",24))
            Title.grid(row=0, column=1)
            temp1 = Label(tab1, text="53.2F", font=("Helvetica",24))
            temp1.grid(row=1, column=2)
            temp1w = Label(tab1, text="Current Temperature Inside")
            temp1w.grid(row=2, column=2)
            temp2 = Label(tab1, text="53.2F")
            temp2.grid(row=3, column=2)
            temp2w = Label(tab1, text="Current Temperature Outside")
            temp2.grid(row=4, column=2)
            mois1 = Label(tab1,text="200")
            mois1.grid(row=5, column=2)
            mois1w = Label(tab1,text="Row 1")
            mois1w.grid(row=6, column=2)
            mois2 = Label(tab1,text="300")
            mois2.grid(row=7, column=2)
            mois2w = Label(tab1,text="Row 2")
            mois2w.grid(row=8, column=2)
            mois2 = Label(tab1,text="255")
            mois2.grid(row=9, column=2)
            mois2w = Label(tab1,text="Row 3")
            mois2w.grid(row=10, column=2)
                    
            # Tab 2
            tab_control.add(tab2, text='Controls')
            # Buttons
            quitButton = Button(tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            quitButton.grid(row=0, column=3)
            fertigateButton = Button(tab2, text = 'Fertigate', command=self.fertigate,bg="green", fg="white", height = 10, width = 20)
            fertigateButton.grid(row=1, column=1)
            waterButton = Button(tab2, text = 'Water', command=self.water, bg="blue", fg="white", height = 10, width = 20)
            waterButton.grid(row=1, column=2)
            heatButton = Button(tab2, text = 'Heat',command=self.heat, bg="orange", fg="white", height = 10, width = 20)
            heatButton.grid(row=1, column=3)
                    
            # Tab 3
            tab_control.add(tab3, text='Error Status')
            # Buttons
            quitButton = Button(tab3, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            quitButton.grid(row=0, column=1, sticky=E)
            # Picture
            errorPic = tk.PhotoImage(file="error.gif")
            w1 = tk.Label(tab3,image=errorPic)
            w1.image = errorPic  # keep a reference!
            w1.grid(row=1, column=1)
            
            tab_control.pack(expand=1, fill='both')
            # Tab 4
            tab_control.add(tab4, text='Maintenance')
            quitButton = Button(tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            quitButton.grid(row=0, column=3)
            
            # Graphs
            style.use('ggplot')
            # Temp Graph
            fig1 = plt.figure(figsize=(10, 6), dpi=100)
            ax1 = fig1.add_subplot(2, 1, 1)
            ax1.set_ylim(0, 150)
            ax1.set_title('Temperature', fontsize=16)
            ax1.legend(('Temp Inside','Temp Outside'), loc='upper right', shadow=True)
            # Moisture Graph
            #fig2 = plt.figure(figsize=(10, 3), dpi=100)
            ax2 = fig1.add_subplot(2, 1, 2)
            ax2.set_ylim(0, 150)
            ax2.set_title('Moisture', fontsize=16)
            ax2.legend(('Row 1','Row 2','Row 3'), loc='upper right', shadow=True)
            # Data
            time = []
            insideTemp = []
            outsideTemp = []
            time_rows = []
            row1 = []
            row2 = []
            row3 = []

            def animate1(i, time, insideTemp, outsideTemp, row1, row2, row3):
                dataI = comm.getGraphData()
                dataO = comm.getGraphData()
                
                time.append(dt.datetime.now().strftime('%H:%M.%f'))
                print("animate1: time", time)
                print("dataI: ", dataI, "insidetemp: ", insideTemp)
                insideTemp.append(dataI[0])
                print("animate1: insideTemp", insideTemp)
                outsideTemp.append(dataO[0])
                print("animate1: outsideTemp", outsideTemp)

                data1 = comm.getGraphData()
                data2 = comm.getGraphData()
                data3 = comm.getGraphData()
                print("animate1: time", time)
                row1.append(data1[0])
                print("animate1: row1", row1)
                row2.append(data2[0])
                print("animate1: row2", row2)
                row3.append(data3[0])
                print("animate1: row3", row3)
 
                time = time[-10:]
                insideTemp = insideTemp[-10:]
                outsideTemp = outsideTemp[-10:]
                row1 = row1[-10:]
                row2 = row2[-10:]
                row3 = row3[-10:]

                ax1.clear()
                ax1.plot(time, insideTemp, time, outsideTemp)
                ax2.clear()
                ax2.plot(time, row1, time, row2, time, row3)

            plotcanvas1 = FigureCanvasTkAgg(fig1, tab1)
            plotcanvas1.get_tk_widget().grid(column=1, row=1)
            ani1 = animation.FuncAnimation(fig1, animate1, fargs=(time, insideTemp, outsideTemp, row1, row2, row3),interval=3000, blit=False)
            
            '''#def animate2(i, time, insideTemp, outsideTemp, row1, row2, row3):
                #time.sleep(1)
                print("animate2: time", time)
                print("animate2: row1", row1)
                print("animate2: row2", row2)
                print("animate2: row3", row3)

                #while (flag =
                ax2.clear()
                ax2.plot(time, row1, time, row2, time, row3)'''
            

            '''plotcanvas1 = FigureCanvasTkAgg(fig1, tab1)
            plotcanvas1.get_tk_widget().grid(column=1, row=1)
            ani1 = animation.FuncAnimation(fig1, animate1, fargs=(time, insideTemp, outsideTemp, row1, row2, row3),interval=3000, blit=False)
            
            
            #plotcanvas2 = FigureCanvasTkAgg(fig2, tab1)
            #plotcanvas2.get_tk_widget().grid(column=1, row=2)
            #ani2 = animation.FuncAnimation(fig2, animate2, fargs=(time, insideTemp, outsideTemp, row1, row2, row3),interval=3000, blit=False)
            '''
            
            root.mainloop()
