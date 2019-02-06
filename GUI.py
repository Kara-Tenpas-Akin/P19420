from tkinter import *           # The Tk package
from tkinter import ttk
from tkinter import messagebox
import Pmw                      # The Python MegaWidget package
import math

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
        quitButton.place(x=430,y=5)
        downloadButton = Button(tab1, command=self.download, text="Download Data")
        downloadButton.place(x=435,y=410)

        # Tab 2
        tab_control.add(tab2, text='Controls')
        quitButton = Button(tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=430,y=5)
        plantButtons = Pmw.ButtonBox(tab2, labelpos='n', label_text='Options')
        plantButtons.pack(fill='both', expand=1, padx=200, pady=200)
        plantButtons.add('Fertigate', command=self.fertigate, bg="green", fg="white")
        plantButtons.add('Water', command=self.water, bg="blue", fg="white")
        plantButtons.add('Heat',command=self.heat, bg="orange", fg="white")

        # Tab 3
        tab_control.add(tab3, text='Error Status')
        quitButton = Button(tab3, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=430,y=5)

        tab_control.pack(expand=1, fill='both')

        # Graph portion
        ncurves = 4                  # draw 4 curves
        npoints = 7                  # use  7 points on each curve

        vector_x = []                 # make vector for x-axis
        vector_y = []
        # fill data in vectors:
        for y in range(ncurves):
            vector_y.append([])      

        for x in range(npoints):    
            vector_x.append(x*0.1)   
            # fill vectors with cool graphs
            for c in range(ncurves): 
                vector_y[c].append(math.sin(c*x*0.5))

        g = Pmw.Blt.Graph(tab1)                     # make a new graph area
        g.pack(expand=1, fill='both',padx=10, pady=100)

        color = ['red', '#ff9900', 'blue', '#00cc00', 'black', 'grey']

        for c in range(ncurves):                
            curvename = 'sin(' + str(c) +'x)'    
            g.line_create(curvename,             
                          xdata=tuple(vector_x),  
                          ydata=tuple(vector_y[c]),
                          color=color[c],          
                          smooth='natural',        
                          linewidth=2,             
                          symbol='')
    
        g.configure(title='Temperature')          # enter a title


        # make s row of buttons
        buttons = Pmw.ButtonBox(tab1, labelpos='n', label_text='Options')
        buttons.pack(fill='both', expand=1, padx=200, pady=10)

        buttons.add('Grid', command=g.grid_toggle)
        buttons.add('Smooth',command=self.smooth)


# Functions

    def client_exit(self):
        exit()

    def download(self):
        messagebox.showinfo('Download Data', 'Download completed.')

    def fertigate(self):
        messagebox.askyesnocancel('Fetigation System', 'Turn on fertigation system?')

    def water(self):
        messagebox.askyesnocancel('Irrigation System', 'Turn on irragation system?')

    def heat(self):
        messagebox.askyesnocancel('Heating System', 'Turn on heating system?')
            
    def smooth(self):
        smoothing = 'linear'
    
        if smoothing == 'linear': smoothing='quadratic'
        elif smoothing == 'quadratic': smoothing='natural'
        elif smoothing == 'natural': smoothing='step'
        else: smoothing = 'linear'

        for curvename in g.element_show():
            g.element_configure(curvename, smooth=smoothing)



# End of code        
root = Tk()

root.geometry("900x800")

app = Window(root)
root.mainloop()  
