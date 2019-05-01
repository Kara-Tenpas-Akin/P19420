#!/usr/bin/env python3
# Graphical User Interface for RIT MSD P19420
# Created by Kara Akin
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

    def __init__(self, name, com2guiQueue, gui2comQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.mycom2guiQueue = com2guiQueue
        self.mygui2comQueue = gui2comQueue
        # Comm to GUI
        self.tempIdata = 0
        self.tempOdata = 0
        self.row1data = 0
        self.row2data = 0
        self.row3data = 0
        self.temp1Error = 0
        self.temp2Error = 0
        self.temp3Error = 0
        self.temp4Error = 0
        self.row1Error = 0
        self.row2Error = 0
        self.row3Error = 0
    
    # Functions
    def client_exit(self):
        #mygui2comQueue = send e-stop to arduino
        self.mygui2comQueue.put("eStop")
        restartArduino = messagebox.showerror("Emergency Stop", "Please Reset Arduino")
    
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
        self.fert_ask.grid_forget()
        self.fert_yes.grid_forget()
        self.fert_no.grid_forget()
        self.water_ask.grid_forget()
        self.water_yes.grid_forget()
        self.water_no.grid_forget()
        self.vent_ask.grid_forget()
        self.vent_yes.grid_forget()
        self.vent_no.grid_forget()
        #mygui2comQueue = send fertigate to ardunio
        self.mygui2comQueue.put("fertOn")

    def no_fertigate(self):
        self.fert_ask.grid_forget()
        self.fert_yes.grid_forget()
        self.fert_no.grid_forget()
        self.water_ask.grid_forget()
        self.water_yes.grid_forget()
        self.water_no.grid_forget()
        self.vent_ask.grid_forget()
        self.vent_yes.grid_forget()
        self.vent_no.grid_forget()

    def yes_water(self):
        self.water_ask.grid_forget()
        self.water_yes.grid_forget()
        self.water_no.grid_forget()
        #mygui2comQueue = send water to ardunio
        self.mygui2comQueue.put("waterOn")

    def no_water(self):
        self.water_ask.grid_forget()
        self.water_yes.grid_forget()
        self.water_no.grid_forget()

    def yes_vent(self):
        self.vent_ask.grid_forget()
        self.vent_yes.grid_forget()
        self.vent_no.grid_forget()
        #mygui2comQueue = send ventilation to ardunio
        self.mygui2comQueue.put("ventOn")

    def no_vent(self):
        self.vent_ask.grid_forget()
        self.vent_yes.grid_forget()
        self.vent_no.grid_forget()
        self.fert_ask.grid_forget()
        self.fert_yes.grid_forget()
        self.fert_no.grid_forget()

    def manualMode(self):
        #mygui2comQueue = send command to put system in manual mode to ardunio
        self.mygui2comQueue.put("manualMode")
        self.manualAllValves.config(bg="yellow")
        self.automateAllValves.config(bg="ivory2")
        self.quitButtonTab4.grid(row=0, column=7, columnspan=7)
        self.w2.grid(row=3, column=0, columnspan=7)
        # Solenoids
        self.masterValveOn= Button(self.tab4, text="Master Valve ON", command=self.masterSolenoidOn, height=5, width=19)
        self.masterValveOn.grid(row=1, column=1, sticky=W)
        self.masterValveOff= Button(self.tab4, text="Master Valve OFF", command=self.masterSolenoidOff, height=5, width=19)
        self.masterValveOff.grid(row=2, column=1, sticky=W)
        self.heaterValveOn= Button(self.tab4, text="Heater Valve ON", command=self.heaterSolenoidOn, height=5, width=19)
        self.heaterValveOn.grid(row=1, column=2, sticky=W)
        self.heaterValveOff= Button(self.tab4, text="Heater Valve OFF", command=self.heaterSolenoidOff, height=5, width=19)
        self.heaterValveOff.grid(row=2, column=2, sticky=W)
        self.waterValveOn= Button(self.tab4, text="Water Valve ON", command=self.waterSolenoidOn, height=5, width=19)
        self.waterValveOn.grid(row=1, column=3, sticky=W)
        self.waterValveOff= Button(self.tab4, text="Water Valve OFF", command=self.waterSolenoidOff, height=5, width=19)
        self.waterValveOff.grid(row=2, column=3, sticky=W)
        self.fertigateValveOn= Button(self.tab4, text="Fertigate Valve ON", command=self.fertigateSolenoidOn, height=5, width=20)
        self.fertigateValveOn.grid(row=1, column=4, sticky=W)
        self.fertigateValveOff= Button(self.tab4, text="Fertigate Valve OFF", command=self.fertigateSolenoidOff, height=5, width=20)
        self.fertigateValveOff.grid(row=2, column=4, sticky=W)
        self.row1ValveOn= Button(self.tab4, text="Row 1 Valve ON", command=self.row1SolenoidOn, height=5, width=19)
        self.row1ValveOn.grid(row=1, column=5, sticky=W)
        self.row1ValveOff= Button(self.tab4, text="Row 1 Valve OFF", command=self.row1SolenoidOff, height=5, width=19)
        self.row1ValveOff.grid(row=2, column=5, sticky=W)
        self.row2ValveOn= Button(self.tab4, text="Row 2 Valve ON", command=self.row2SolenoidOn, height=5, width=19)
        self.row2ValveOn.grid(row=1, column=6, sticky=W)
        self.row2ValveOff= Button(self.tab4, text="Row 2 Valve OFF", command=self.row2SolenoidOff, height=5, width=19)
        self.row2ValveOff.grid(row=2, column=6, sticky=W)
        self.row3ValveOn= Button(self.tab4, text="Row 3 Valve ON", command=self.row3SolenoidOn, height=5, width=20)
        self.row3ValveOn.grid(row=1, column=7, sticky=W)
        self.row3ValveOff= Button(self.tab4, text="Row 3 Valve OFF", command=self.row3SolenoidOff, height=5, width=20)
        self.row3ValveOff.grid(row=2, column=7, sticky=W)


    def automaticMode(self):
        #mygui2comQueue = send command to put system in automatic mode to ardunio
        self.automateAllValves.config(bg="green")
        self.manualAllValves.config(bg="ivory2")
        self.mygui2comQueue.put("autoMode")
        self.masterValveOn.grid_forget()
        self.masterValveOff.grid_forget()
        self.heaterValveOn.grid_forget()
        self.heaterValveOff.grid_forget()
        self.waterValveOn.grid_forget()
        self.waterValveOff.grid_forget()
        self.fertigateValveOn.grid_forget()
        self.fertigateValveOff.grid_forget()
        self.row1ValveOn.grid_forget()
        self.row1ValveOff.grid_forget()
        self.row2ValveOn.grid_forget()
        self.row2ValveOff.grid_forget()
        self.row3ValveOn.grid_forget()
        self.row3ValveOff.grid_forget()

    def masterSolenoidOn(self):
        #mygui2comQueue = send master soleniod on to arduino
        self.mygui2comQueue.put("masterSolOn")
        self.masterValveOn.config(bg="PaleGreen")
        self.masterValveOff.config(bg="ivory2")

    def waterSolenoidOn(self):
        #mygui2comQueue = send water soleniod on to arduino
        self.mygui2comQueue.put("waterSolOn")
        self.waterValveOn.config(bg="PaleGreen")
        self.waterValveOff.config(bg="ivory2")

    def heaterSolenoidOn(self):
        #mygui2comQueue = send heater soleniod on to arduino
        self.mygui2comQueue.put("heatSolOn")
        self.heaterValveOn.config(bg="PaleGreen")
        self.heaterValveOff.config(bg="ivory2")

    def fertigateSolenoidOn(self):
        #mygui2comQueue = send fertigate soleniod on to arduino
        self.mygui2comQueue.put("fertSolOn")
        self.fertigateValveOn.config(bg="PaleGreen")
        self.fertigateValveOff.config(bg="ivory2")

    def row1SolenoidOn(self):
        #mygui2comQueue = send row 1 soleniod on to arduino
        self.mygui2comQueue.put("row1SolOn")
        self.row1ValveOn.config(bg="PaleGreen")
        self.row1ValveOff.config(bg="ivory2")

    def row2SolenoidOn(self):
        #mygui2comQueue = send row 2 soleniod on to arduino
        self.mygui2comQueue.put("row2SolOn")
        self.row2ValveOn.config(bg="PaleGreen")
        self.row2ValveOff.config(bg="ivory2")
        
    def row3SolenoidOn(self):
        #mygui2comQueue = send row 3 soleniod on to arduino
        self.mygui2comQueue.put("row3SolOn")
        self.row3ValveOn.config(bg="PaleGreen")
        self.row3ValveOff.config(bg="ivory2")
        
    def masterSolenoidOff(self):
        #mygui2comQueue = send master soleniod off to arduino
        self.mygui2comQueue.put("masterSolOff")
        self.masterValveOff.config(bg="PaleGreen")
        self.masterValveOn.config(bg="ivory2")
        
    def waterSolenoidOff(self):
        #mygui2comQueue = send water soleniod off to arduino
        self.mygui2comQueue.put("waterSolOff")
        self.waterValveOff.config(bg="PaleGreen")
        self.waterValveOn.config(bg="ivory2")
        
    def heaterSolenoidOff(self):
        #mygui2comQueue = send heater soleniod off to arduino
        self.mygui2comQueue.put("heatSolOff")
        self.heaterValveOff.config(bg="PaleGreen")
        self.heaterValveOn.config(bg="ivory2")
        
    def fertigateSolenoidOff(self):
        #mygui2comQueue = send fertigate soleniod off to arduino
        self.mygui2comQueue.put("fertSolOff")
        self.fertigateValveOff.config(bg="PaleGreen")
        self.fertigateValveOn.config(bg="ivory2")
        
    def row1SolenoidOff(self):
        #mygui2comQueue = send row 1 soleniod off to arduino
        self.mygui2comQueue.put("row1SolOff")
        self.row1ValveOff.config(bg="PaleGreen")
        self.row1ValveOn.config(bg="ivory2")
        
    def row2SolenoidOff(self):
        #mygui2comQueue = send row 2 soleniod off to arduino
        self.mygui2comQueue.put("row2SolOff")
        self.row2ValveOff.config(bg="PaleGreen")
        self.row2ValveOn.config(bg="ivory2")
        
    def row3SolenoidOff(self):
        #mygui2comQueue = send row 3 soleniod off to arduino
        self.mygui2comQueue.put("row3SolOff")
        self.row3ValveOff.config(bg="PaleGreen")
        self.row3ValveOn.config(bg="ivory2")
        
    def run(self):
        while(True):
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
            self.w1.grid(row=4, column=1, columnspan=2, sticky=E, padx=90)
            
            # Tab 4
            self.tab_control.add(self.tab4, text='Maintenance')
            self.quitButtonTab4 = Button(self.tab4, text="Emergency Stop", command=self.client_exit, bg="red", fg="white",height = 5, width = 20)
            self.quitButtonTab4.grid(row=0, column=5)
            # Picture of Valve Chart for Maintenance page
            pipingPic = tk.PhotoImage(file="Piping_Diagram.gif")
            self.w2 = tk.Label(self.tab4,image=pipingPic)
            self.w2.image = pipingPic  # keep a reference!
            self.w2.grid(row=3, column=0, columnspan=7)
            # Buttons
            # Mode
            self.automateAllValves = Button(self.tab4, text="Automatic Mode", command=self.automaticMode, height=5, width=19)
            self.automateAllValves.grid(row=0, column=1)
            self.manualAllValves = Button(self.tab4, text="Manual Mode", command=self.manualMode, height=5, width=19)
            self.manualAllValves.grid(row=0, column=2)
            
            self.tab_control.pack(expand=1, fill='both')
            
            # Graphs
            style.use('ggplot')
            self.fig1 = plt.figure(figsize=(11, 6))
            # Temp Graph
            self.ax1 = self.fig1.add_subplot(2, 1, 1)
            # Moisture Graph
            self.ax2 = self.fig1.add_subplot(2, 1, 2)

            timeData = []
            insideTemp = []
            outsideTemp = []
            row1 = []
            row2 = []
            row3 = []
            
            self.plotcanvas1 = FigureCanvasTkAgg(self.fig1, self.tab1)
            self.plotcanvas1.get_tk_widget().grid(column=1, row=1, rowspan=12)
            self.ani1 = animation.FuncAnimation(self.fig1, self.animate1, fargs=(timeData, insideTemp, outsideTemp, row1, row2, row3),interval=900000, blit=False)
                
            import time
            while True:
                self.root.update_idletasks()
                self.root.update()
                # Check queue here
                try:
                    self.tempIdata, self.tempOdata, self.row1data, self.row2data, self.row3data, self.temp1Error, self.temp2Error, self.temp3Error, self.temp4Error, self.row1Error, self.row2Error, self.row3Error = self.mycom2guiQueue.get(block=False, timeout=None)
                    #print(".")
                except:
                    #print("*")
                    time.sleep(1)
                    #pass
                # Error handling
                if self.temp1Error == 1:
                    self.tempErrorLabel = Label(self.tab3, text="  Temperature Sensor Error  ", font=("Helvetica",24), fg='red')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.temp2Error == 1: 
                    self.tempErrorLabel = Label(self.tab3, text="  Temperature Sensor Error  ", font=("Helvetica",24), fg='red')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.temp3Error == 1: 
                    self.tempErrorLabel = Label(self.tab3, text="  Temperature Sensor Error"  , font=("Helvetica",24), fg='red')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.temp4Error == 1: 
                    self.tempErrorLabel = Label(self.tab3, text="  Temperature Sensor Error  ", font=("Helvetica",24), fg='red')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.row1Error == 1: 
                    self.row1ErrorLabel = Label(self.tab3, text="Row 1 Moisture Sensor Error", font=("Helvetica",24), fg='red')
                    self.row1ErrorLabel.grid(row=1, column=1)
                if self.row2Error == 1: 
                    self.row2ErrorLabel = Label(self.tab3, text="Row 2 Moisture Sensor Error", font=("Helvetica",24), fg='red')
                    self.row2ErrorLabel.grid(row=2, column=1)
                if self.row3Error == 1: 
                    self.row3ErrorLabel = Label(self.tab3, text="Row 3 Moisture Sensor Error", font=("Helvetica",24), fg='red')
                    self.row3ErrorLabel.grid(row=3, column=1)
                # Error Clearing
                if self.temp1Error == 0:
                    self.tempErrorLabel = Label(self.tab3, text="  Temperature Sensors Good  ", font=("Helvetica",24), fg='green')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.temp2Error == 0: 
                    self.tempErrorLabel = Label(self.tab3, text="  Temperature Sensors Good  ", font=("Helvetica",24), fg='green')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.temp3Error == 0: 
                    self.tempErrorLabel = Label(self.tab3, text="  Temperature Sensors Good  ", font=("Helvetica",24), fg='green')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.temp4Error == 0: 
                    self.tempErrorLabel = Label(self.tab3, text="Temperature Sensors Good", font=("Helvetica",24), fg='green')
                    self.tempErrorLabel.grid(row=1, column=2, rowspan=3)
                if self.row1Error == 0: 
                    self.row1ErrorLabel = Label(self.tab3, text="Row 1 Moisture Sensor Good", font=("Helvetica",24), fg='green')
                    self.row1ErrorLabel.grid(row=1, column=1)
                if self.row2Error == 0: 
                    self.row2ErrorLabel = Label(self.tab3, text="Row 2 Moisture Sensor Good", font=("Helvetica",24), fg='green')
                    self.row2ErrorLabel.grid(row=2, column=1)
                if self.row3Error == 0: 
                    self.row3ErrorLabel = Label(self.tab3, text="Row 3 Moisture Sensor Good", font=("Helvetica",24), fg='green')
                    self.row3ErrorLabel.grid(row=3, column=1)
                #time.sleep(1)


    def animate1(self, i, timeData, insideTemp, outsideTemp, row1, row2, row3):
        # Get new data point 
        dataI = int(self.tempIdata)
        dataO = int(self.tempOdata)
        data1 = int(self.row1data)
        data2 = int(self.row2data)
        data3 = int(self.row3data)
        # Updating Current Data Labels
        if dataI == -99:
            self.temp1 = Label(self.tab1, text="ERR", font=("Helvetica",24))
        else:
            self.temp1 = Label(self.tab1, text=" %d F " % dataI, font=("Helvetica",24))
        if dataO == -99:
            self.temp2 = Label(self.tab1, text=" ERR ", font=("Helvetica",24))
        else:
            self.temp2 = Label(self.tab1, text=" %d F " % dataO, font=("Helvetica",24))
        if data1 == -99:
           self.mois1 = Label(self.tab1, text=" ERR ", font=("Helvetica",24))
        else:
           self.mois1 = Label(self.tab1,text=" %d " % data1, font=("Helvetica",24))
        if data2 == -99:
            self.mois2 = Label(self.tab1, text=" ERR ", font=("Helvetica",24))
        else:
            self.mois2 = Label(self.tab1,text=" %d " % data2, font=("Helvetica",24))
        if data3 ==-99:
            self.mois3 = Label(self.tab1, text=" ERR ", font=("Helvetica",24))
        else:
            self.mois3 = Label(self.tab1,text=" %d " % data3, font=("Helvetica",24))
        self.temp1.grid(row=1, column=2)
        self.temp2.grid(row=3, column=2)
        self.mois1.grid(row=5, column=2)
        self.mois2.grid(row=7, column=2)
        self.mois3.grid(row=9, column=2)
        # Append new data point to existing list
        insideTemp.append(dataI)
        outsideTemp.append(dataO)
        row1.append(data1)
        row2.append(data2)
        row3.append(data3)
        timeData.append(dt.datetime.now().strftime("%m/%d %H:%M"))
        # Only plot last 10 data points
        time_plot = timeData[-10:]
        insideTemp_plot = insideTemp[-10:]
        outsideTemp_plot = outsideTemp[-10:]
        row1_plot = row1[-10:]
        row2_plot = row2[-10:]
        row3_plot = row3[-10:]
        # Plot the data
        self.ax1.clear()
        self.ax1.plot(time_plot, insideTemp_plot, 'g', time_plot, outsideTemp_plot, 'b')
        self.ax2.clear()
        self.ax2.plot(time_plot, row1_plot, 'c', time_plot, row2_plot, 'm', time_plot, row3_plot, 'y')
        # Configure the graphs
        self.ax1.set_ylim(-10, 120)
        self.ax1.set_title('Temperature', fontsize=16)
        self.ax1.legend(('Temp Inside','Temp Outside'), loc='upper right', shadow=True)
        self.ax1.xaxis.set_tick_params(rotation=45, labelcolor='white')
        self.ax2.set_ylim(0, 1050)
        self.ax2.set_title('Moisture', fontsize=16)
        self.ax2.legend(('Row 1','Row 2','Row 3'), loc='upper right', shadow=True)
        self.ax2.xaxis.set_tick_params(rotation=45)











                
