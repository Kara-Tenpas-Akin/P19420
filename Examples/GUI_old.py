from tkinter import *           # The Tk package
from tkinter import ttk
from tkinter import messagebox
#from tkinter import PhotoImage
import tkinter as tk
import Pmw                      # The Python MegaWidget package
import math
import csv
import threading
import time

root = Tk()

#class Window(Frame):

   # def __init__(self, master=None):
   #     Frame.__init__(self, master)                 
   #     self.master = master
   #     self.init_window()

    #Creation of init_window
   # def init_window(self):    
   #     self.master.title("GUI")
   #     self.pack(fill=BOTH, expand=1)

        # Creation of Tabs
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)

# Tab 1
        tab_control.add(tab1, text='Status')
        # Buttons
        quitButton = Button(tab1, text="Emergency Stop", command=client_exit, bg="red", fg="white", height = 5, width = 20)
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
        
        # Graphs
        # Temp Graph
        g = Pmw.Blt.Graph(tab1)                     
        g.grid(row=1, column=1)
        # Moisture Graph
        gg = Pmw.Blt.Graph(tab1)                     
        gg.grid(row=2, column=1)
        # Buttons to control graphs + other
        buttons = Pmw.ButtonBox(tab1, labelpos='n', label_text='Options')
        buttons.grid(row=3, column=1)
        buttons.add('Refresh', command=self.refresh)
        buttons.add('Temp Grid', command=g.grid_toggle)
        buttons.add('Moisture Grid', command=gg.grid_toggle)
        buttons.add('Download Data', command=self.download)

        # Configure Grid
        
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

        if MsgBox == 'yes':
            fertON = Label(tab2, text="ON")
            fertON.grid(row=4, column=1)
        if MsgBox == 'no':
            fertOFF = Label(tab2, text="OFF")
            fertOFF.grid(row=4, column=1)
        else:
            fertWhat = Label(tab2, text="what")
            fertWhat.grid(row=4, column=1)
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



        
# Graph portion
        list_x = []                 # make lists for data set 1
        list_y = []
        list_x2 = []                 # make lists for data set 2
        list_y2 = []
        list_x3 = []                 # make lists for data set 3
        list_y3 = []
        with open('data.txt','r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                list_x.append(int(row[0]))
                list_y.append(int(row[1]))

        with open('data2.txt','r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                list_x2.append(int(row[0]))
                list_y2.append(int(row[1]))

        with open('data3.txt','r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                list_x3.append(int(row[0]))
                list_y3.append(int(row[1]))
        
        color = ['red', '#ff9900', 'blue', '#00cc00', 'black', 'grey']

        #First line              
        curvename = str('Inside Temp')
        g.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[0],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
        #Second line               
        curvename = str('Outside Temp')
        g.line_create(curvename,             
                        xdata=tuple(list_x2),  
                        ydata=tuple(list_y2),
                        color=color[1],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
    
        g.configure(title='Temperature', height=300, width=1000)  


        color = ['blue', '#00cc00', 'grey']

        #First line                
        curvename = str('Row 1')
        gg.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[0],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
        #Second line               
        curvename = str('Row 2')
        gg.line_create(curvename,             
                        xdata=tuple(list_x2),  
                        ydata=tuple(list_y2),
                        color=color[1],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
        #Third line              
        curvename = str('Row 3')
        gg.line_create(curvename,             
                        xdata=tuple(list_x3),  
                        ydata=tuple(list_y3),
                        color=color[2],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
        gg.configure(title='Moisture', height=300, width=1000)   


# Functions

    def client_exit(self):
        exit()

    def download(self):
        messagebox.showinfo('Download Data', 'Download completed.')

    def refresh(self):
        messagebox.showinfo('Refresh', 'Refresh of graphs completed.')

    def fertigate(Frame):
        MsgBoxF = messagebox.askyesnocancel('Fetigation System', 'Turn on fertigation system?')
        return MsgBoxF

    def water(self):
        messagebox.askyesnocancel('Irrigation System', 'Turn on irragation system?')

    def heat(self):
        messagebox.askyesnocancel('Heating System', 'Turn on heating system?')
        
# Uncomment when threading

#class guiThread1(threading.Thread):
    #def __init__(self,name):
        #threading.Thread.__init__(self)
        #self.name = name
        #print("GUI thread is initialized")

    #def run(self):
        # End of code        
        #root = Tk()
        #app = Window(root)
        #root.mainloop()  
        #while(True):
            #print("GUI Thread is running")
            #time.sleep(2)

#root = Tk()
#app = Window(root)
root.mainloop() 
