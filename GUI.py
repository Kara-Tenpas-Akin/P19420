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

    def __init__(self, name, threadQueue):
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
    
    def fertigate(self):
        self.fert_ask = Label(self.tab2, text="Are you sure?", font=("Helvetica",24))
        self.fert_ask.grid(row=2, column=1)
        self.fert_yes = Button(self.tab2, text="Yes", command=self.yes_fertigate, height=5, width=10)
        self.fert_yes.grid(row=3, column=1, sticky=W, padx=25, pady=25)
        self.fert_no = Button(self.tab2, text="No", command=self.no_fertigate, height=5, width=10)
        self.fert_no.grid(row=3, column=1, sticky=E, padx=25, pady=25)
    
    def water(self):
        self.water_ask = Label(self.tab2, text="Are you sure?", font=("Helvetica",24))
        self.water_ask.grid(row=2, column=2)
        self.water_yes = Button(self.tab2, text="Yes", command=self.yes_water, height=5, width=10)
        self.water_yes.grid(row=3, column=2, sticky=W, padx=25, pady=25)
        self.water_no = Button(self.tab2, text="No", command=self.no_water, height=5, width=10)
        self.water_no.grid(row=3, column=2, sticky=E, padx=25, pady=25)
    
    def vent(self):
        self.vent_ask = Label(self.tab2, text="Are you sure?", font=("Helvetica",24))
        self.vent_ask.grid(row=2, column=3)
        self.vent_yes = Button(self.tab2, text="Yes", command=self.yes_vent, height=5, width=10)
        self.vent_yes.grid(row=3, column=3, sticky=W, padx=25, pady=25)
        self.vent_no = Button(self.tab2, text="No", command=self.no_vent, height=5, width=10)
        self.vent_no.grid(row=3, column=3, sticky=E, padx=25, pady=25)

    def yes_fertigate(self):
        #myqueue = send fertigate to ardunio
        self.fert_ask.grid_forget()
        self.fert_yes.grid_forget()
        self.fert_no.grid_forget()
        print("yes")

    def no_fertigate(self):
        self.fert_ask.grid_forget()
        self.fert_yes.grid_forget()
        self.fert_no.grid_forget()
        print("no")

    def yes_water(self):
        #myqueue = send fertigate to ardunio
        self.water_ask.grid_forget()
        self.water_yes.grid_forget()
        self.water_no.grid_forget()
        print("yes")

    def no_water(self):
        self.water_ask.grid_forget()
        self.water_yes.grid_forget()
        self.water_no.grid_forget()
        print("no")

    def yes_vent(self):
        #myqueue = send fertigate to ardunio
        self.vent_ask.grid_forget()
        self.vent_yes.grid_forget()
        self.vent_no.grid_forget()
        print("yes")

    def no_vent(self):
        self.vent_ask.grid_forget()
        self.vent_yes.grid_forget()
        self.vent_no.grid_forget()
        print("no")

    def run(self):
        while(True):

            #root = Tk()
            
            #define root and tabs
            self.root = Tk()
            self.root.title('Blackberry High Tunnel')
            self.tab_control = ttk.Notebook(self.root)
            self.tab1 = ttk.Frame(self.tab_control)
            self.tab2 = ttk.Frame(self.tab_control)
            self.tab3 = ttk.Frame(self.tab_control)
            self.tab4 = ttk.Frame(self.tab_control)
            
            # Tab 1
            self.tab_control.add(self.tab1, text='Status')
            # Buttons
            quitButton = Button(self.tab1, text="Emergency Stop", command=self.client_exit, bg="red", fg="white", height = 5, width = 20)
            quitButton.grid(row=0, column=2, sticky=W+E+N+S)
            # Text
            Title = Label(self.tab1, text="Durgin Family Farms Blackberry Hightunnel", font=("Helvetica",24))
            Title.grid(row=0, column=1)
            temp1w = Label(self.tab1, text="Current Temperature \n Inside",font=("Helvetica",12))
            temp1w.grid(row=2, column=2)
            temp2w = Label(self.tab1, text="Current Temperature\n Outside",font=("Helvetica",12))
            temp2w.grid(row=4, column=2)
            mois1w = Label(self.tab1,text="Row 1",font=("Helvetica",12))
            mois1w.grid(row=6, column=2)
            mois2w = Label(self.tab1,text="Row 2",font=("Helvetica",12))
            mois2w.grid(row=8, column=2)
            mois3w = Label(self.tab1,text="Row 3",font=("Helvetica",12))
            mois3w.grid(row=10, column=2)

            # Tab 2
            self.tab_control.add(self.tab2, text='Controls')
            # Buttons
            quitButton = Button(self.tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            quitButton.grid(row=0, column=3, sticky=E)
            fertigateButton = Button(self.tab2, text = 'Fertigate', command=self.fertigate,bg="green", fg="white", height = 10, width = 20)
            fertigateButton.grid(row=1, column=1, padx=120, pady=75)
            waterButton = Button(self.tab2, text = 'Water', command=self.water, bg="blue", fg="white", height = 10, width = 20)
            waterButton.grid(row=1, column=2, padx=120, pady=75)
            ventButton = Button(self.tab2, text = 'Ventilation',command=self.vent, bg="orange", fg="white", height = 10, width = 20)
            ventButton.grid(row=1, column=3, padx=120, pady=75)
                    
            # Tab 3
            self.tab_control.add(self.tab3, text='Error Status')
            # Buttons
            self.quitButton = Button(self.tab3, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            self.quitButton.grid(row=0, column=2, sticky=E)
            # Picture of Sensors for Error page
            errorPic = tk.PhotoImage(file="error.gif")
            self.w1 = tk.Label(self.tab3,image=errorPic)
            self.w1.image = errorPic  # keep a reference!
            self.w1.grid(row=1, column=1, columnspan=2, sticky=E, padx=90, pady=60)
            
            # Tab 4
            self.tab_control.add(self.tab4, text='Maintenance')
            self.quitButton = Button(self.tab4, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            self.quitButton.grid(row=0, column=2, sticky=E)
            # Picture of Valve Chart for Maintenance page
            pipingPic = tk.PhotoImage(file="Piping_Diagram.gif")
            self.w2 = tk.Label(self.tab4,image=pipingPic)
            self.w2.image = pipingPic  # keep a reference!
            self.w2.grid(row=1, column=1, columnspan=2, sticky=E, padx=90, pady=60)

            self.tab_control.pack(expand=1, fill='both')
            
            # Graphs
            style.use('ggplot')
            self.fig1 = plt.figure(figsize=(11, 6))
            # Temp Graph
            self.ax1 = self.fig1.add_subplot(2, 1, 1)
            # Moisture Graph
            self.ax2 = self.fig1.add_subplot(2, 1, 2)

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
                self.temp1 = Label(self.tab1, text="%d F" % temp1_data, font=("Helvetica",24))
                self.temp1.grid(row=1, column=2)
                self.temp2 = Label(self.tab1, text="%d F" % temp2_data, font=("Helvetica",24))
                self.temp2.grid(row=3, column=2)
                self.mois1 = Label(self.tab1,text="%d" % row1_data, font=("Helvetica",24))
                self.mois1.grid(row=5, column=2)
                self.mois2 = Label(self.tab1,text="%d" % row2_data, font=("Helvetica",24))
                self.mois2.grid(row=7, column=2)
                self.mois3 = Label(self.tab1,text="%d" % row3_data, font=("Helvetica",24))
                self.mois3.grid(row=9, column=2)
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
                self.ax1.clear()
                self.ax1.plot(time_plot, insideTemp_plot, 'g', time_plot, outsideTemp_plot, 'b')
                self.ax2.clear()
                self.ax2.plot(time_plot, row1_plot, 'c', time_plot, row2_plot, 'm',time_plot, row3_plot, 'y')
                # Configure the graphs
                self.ax1.set_ylim(0, 150)
                self.ax1.set_title('Temperature', fontsize=16)
                self.ax1.legend(('Temp Inside','Temp Outside'), loc='upper right', shadow=True)
                self.ax1.xaxis.set_tick_params(rotation=45, labelcolor='white')
                self.ax2.set_ylim(0, 150)
                self.ax2.set_title('Moisture', fontsize=16)
                self.ax2.legend(('Row 1','Row 2','Row 3'), loc='upper right', shadow=True)
                self.ax2.xaxis.set_tick_params(rotation=45)

                

            self.plotcanvas1 = FigureCanvasTkAgg(self.fig1, self.tab1)
            self.plotcanvas1.get_tk_widget().grid(column=1, row=1, rowspan=10)
            self.ani1 = animation.FuncAnimation(self.fig1, animate1, fargs=(time, insideTemp, outsideTemp, row1, row2, row3),interval=3000, blit=False)
            
           
            
            self.root.mainloop()
