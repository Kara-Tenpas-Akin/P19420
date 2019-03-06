
from tkinter import *           # The Tk package
from tkinter import ttk
from tkinter import messagebox
from tkinter import Tk
import Pmw                      # The Python MegaWidget package
import math
import csv
import threading
import time
from PIL import Image


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):    
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)

        # Creation of Tabs
        tab_control = ttk.Notebook(self)
        
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)

        # Tab 1
        tab_control.add(tab1, text='Status')
        # Buttons
        quitButton = Button(tab1, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.pack(expand=1, fill='y',padx=50, pady=50)
        quitButton.place(x=1125,y=5)

        # Tab 2
        tab_control.add(tab2, text='Controls')
        # Buttons
        quitButton = Button(tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=1125,y=5)
        fertigateButton = Button(tab2, text = 'Fertigate', command=self.fertigate, bg="green", fg="white", height = 10, width = 20)
        fertigateButton.place(x=100,y=300)
        waterButton = Button(tab2, text = 'Water', command=self.water, bg="blue", fg="white", height = 10, width = 20)
        waterButton.place(x=550,y=300)
        heatButton = Button(tab2, text = 'Heat',command=self.heat, bg="orange", fg="white", height = 10, width = 20)
        heatButton.place(x=1000,y=300)
        
        # Tab 3
        tab_control.add(tab3, text='Error Status')
        # Buttons
        quitButton = Button(tab3, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=1125,y=5)
        everythingButton = Button(tab3, text="Everything is working", bg="green", fg="white", height = 30, width = 50)
        everythingButton.place(x=550,y=200)
        # Picture
        canvas = Canvas(tab3, width = 300, height = 300)      
        canvas.pack()      
        img = PhotoImage(file="Error.gif")      
        canvas.create_image(20,20, anchor=NW, image=img)  

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
        
        # make a new graph area
        g = Pmw.Blt.Graph(tab1)                     
        g.pack(expand=1, fill='both',padx=10, pady=40)

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
    
        g.configure(title='Temperature',height=200)  

        # make a new graph area
        gg = Pmw.Blt.Graph(tab1)                     
        gg.pack(expand=1, fill='both',padx=10, pady=10)

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
        gg.configure(title='Moisture',height=200) 

        
        # make a row of buttons
        buttons = Pmw.ButtonBox(tab1, labelpos='n', label_text='Options')
        buttons.pack(fill='both', expand=0, padx=200, pady=10)
        buttons.add('Refresh', command=self.refresh)
        buttons.add('Temp Grid', command=g.grid_toggle)
        buttons.add('Moisture Grid', command=gg.grid_toggle)
        buttons.add('Download Data', command=self.download)

# Functions

    def client_exit(self):
        exit()

    def download(self):
        messagebox.showinfo('Download Data', 'Download completed.')

    def refresh(self):
        messagebox.showinfo('Refresh', 'Refresh of graphs completed.')

    def fertigate(self):
        messagebox.askyesnocancel('Fetigation System', 'Turn on fertigation system?')

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

root = Tk()
app = Window(root)
root.mainloop()  

