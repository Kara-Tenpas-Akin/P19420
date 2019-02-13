from tkinter import *           # The Tk package
from tkinter import ttk
from tkinter import messagebox
import Pmw                      # The Python MegaWidget package
import math
import csv

ncurves = 4                  # draw 4 curves
npoints = 7                  # use  7 points on each curve

vector_x = []                 # make vector for x-axis
vector_y = []

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
        quitButton = Button(tab1, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.pack(expand=1, fill='y',padx=50, pady=50)
        quitButton.place(x=555,y=5)

        # Tab 2
        tab_control.add(tab2, text='Controls')
        quitButton = Button(tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=430,y=5)
        plantButtons = Pmw.ButtonBox(tab2, labelpos='n', label_text='Options')
        plantButtons.pack(fill='both', expand=1, padx=200, pady=200)
        #plantButtons.place(x=430,y=5)
        plantButtons.add('Fertigate', command=self.fertigate, bg="green", fg="white")
        plantButtons.add('Water', command=self.water, bg="blue", fg="white")
        plantButtons.add('Heat',command=self.heat, bg="orange", fg="white")

        # Tab 3
        tab_control.add(tab3, text='Error Status')
        quitButton = Button(tab3, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=430,y=5)

        tab_control.pack(expand=1, fill='both')

        # Graph portion

        list_x = []                 # make vector for x-axis
        list_y = []
        list_x2 = []                 # make vector for x-axis
        list_y2 = []

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
        
        # make a new graph area
        g = Pmw.Blt.Graph(tab1)                     
        g.pack(expand=1, fill='both',padx=10, pady=40)

        color = ['red', '#ff9900', 'blue', '#00cc00', 'black', 'grey']

        #First line              
        curvename = str('Temp 1')
        g.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[0],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
        #Second line               
        curvename = str('Temp 2')
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

        color = ['blue', '#00cc00', 'black', 'grey']

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
    
        gg.configure(title='Moisture',height=200) 

        
        # make a row of buttons
        buttons = Pmw.ButtonBox(tab1, labelpos='n', label_text='Options')
        buttons.pack(fill='both', expand=0, padx=200, pady=10)
        buttons.add('Refresh', command=self.refresh)
        buttons.add('Grid', command=g.grid_toggle)
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



# End of code        
root = Tk()

#root.geometry("900x800")

app = Window(root)
root.mainloop()  
