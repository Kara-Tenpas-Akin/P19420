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
from queue import Queue

class guiThread1(threading.Thread):
    def __init__(self,name, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.guiQueue = threadQueue
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
            quitButton.grid(row=0, column=2, sticky=W+E+N+S)
            # Text
            Title = Label(tab1, text="Durgin Family Farms Blackberry Hightunnel", font=("Helvetica",24))
            Title.grid(row=0, column=1)
            temp1w = Label(tab1, text="Current Temperature \n Inside",font=("Helvetica",12))
            temp1w.grid(row=2, column=2)
            temp2w = Label(tab1, text="Current Temperature\n Outside",font=("Helvetica",12))
            temp2w.grid(row=4, column=2)
            mois1w = Label(tab1,text="Row 1",font=("Helvetica",12))
            mois1w.grid(row=6, column=2)
            mois2w = Label(tab1,text="Row 2",font=("Helvetica",12))
            mois2w.grid(row=8, column=2)
            mois3w = Label(tab1,text="Row 3",font=("Helvetica",12))
            mois3w.grid(row=10, column=2)


            # Tab 2
            tab_control.add(tab2, text='Controls')
            # Buttons
            quitButton = Button(tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            quitButton.grid(row=0, column=3)
            fertigateButton = Button(tab2, text = 'Fertigate', command=self.fertigate,bg="green", fg="white", height = 10, width = 20)
            fertigateButton.grid(row=1, column=1)
            waterButton = Button(tab2, text = 'Water', command=self.water, bg="blue", fg="white", height = 10, width = 20)
            waterButton.grid(row=1, column=2)
            heatButton = Button(tab2, text = 'Ventilation',command=self.heat, bg="orange", fg="white", height = 10, width = 20)
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
            fig1 = plt.figure(figsize=(11, 6))
            ax1 = fig1.add_subplot(2, 1, 1)
            
            # Moisture Graph
            ax2 = fig1.add_subplot(2, 1, 2)

            # Data
            time = []
            insideTemp = []
            outsideTemp = []
            time_rows = []
            row1 = []
            row2 = []
            row3 = []

            def animate1(i, time, insideTemp, outsideTemp, row1, row2, row3):
                # Get new data point 
                dataI = comm.getGraphData()
                dataO = comm.getGraphData()
                data1 = comm.getGraphData()
                data2 = comm.getGraphData()
                data3 = comm.getGraphData()
                temp1_data = dataI[0]
                temp2_data = dataO[0]
                row1_data = data1[0]
                row2_data = data2[0]
                row3_data = data3[0]
                # Updating Current Data Labels
                temp1 = Label(tab1, text="%d F" % temp1_data, font=("Helvetica",24))
                temp1.grid(row=1, column=2)
                temp2 = Label(tab1, text="%d F" % temp2_data, font=("Helvetica",24))
                temp2.grid(row=3, column=2)
                mois1 = Label(tab1,text="%d" % row1_data, font=("Helvetica",24))
                mois1.grid(row=5, column=2)
                mois2 = Label(tab1,text="%d" % row2_data, font=("Helvetica",24))
                mois2.grid(row=7, column=2)
                mois3 = Label(tab1,text="%d" % row3_data, font=("Helvetica",24))
                mois3.grid(row=9, column=2)
                # Append new data point to existing list
                insideTemp.append(dataI[0])
                outsideTemp.append(dataO[0])
                row1.append(data1[0])
                row2.append(data2[0])
                row3.append(data3[0])
                time.append(dt.datetime.now().strftime("%m/%d %H:%M:%S"))
                # Only plot last 10 data points
                time_plot = time[-10:]
                insideTemp_plot = insideTemp[-10:]
                outsideTemp_plot = outsideTemp[-10:]
                row1_plot = row1[-10:]
                row2_plot = row2[-10:]
                row3_plot = row3[-10:]
                # Plot the data
                ax1.clear()
                ax1.plot(time_plot, insideTemp_plot, 'g', time_plot, outsideTemp_plot, 'b')
                ax2.clear()
                ax2.plot(time_plot, row1_plot, 'c', time_plot, row2_plot, 'm',time_plot, row3_plot, 'y')
                # Configure the graphs
                ax1.set_ylim(0, 150)
                ax1.set_title('Temperature', fontsize=16)
                ax1.legend(('Temp Inside','Temp Outside'), loc='upper right', shadow=True)
                ax1.xaxis.set_tick_params(rotation=45, labelcolor='white')
                ax2.set_ylim(0, 150)
                ax2.set_title('Moisture', fontsize=16)
                ax2.legend(('Row 1','Row 2','Row 3'), loc='upper right', shadow=True)
                ax2.xaxis.set_tick_params(rotation=45)

                

            plotcanvas1 = FigureCanvasTkAgg(fig1, tab1)
            plotcanvas1.get_tk_widget().grid(column=1, row=1, rowspan=10)
            ani1 = animation.FuncAnimation(fig1, animate1, fargs=(time, insideTemp, outsideTemp, row1, row2, row3),interval=3000, blit=False)
            
           
            
            root.mainloop()
