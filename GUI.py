from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import Pmw
Pmw.initialise(root)

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):    
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
    
        #lbl = Label(self, text="Blackberry High Tunnel")
        #lbl.grid(column=0, row=0)

        tab_control = ttk.Notebook(self)
 
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Status')
        quitButton = Button(tab1, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=430,y=5)
        downloadButton = Button(tab1, command=self.download, text="Download Data")
        downloadButton.place(x=435,y=410)
        
        tab_control.add(tab2, text='Controls')
        quitButton = Button(tab2, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=430,y=5)
        fertButton = Button(tab2, text="Fertigate", command=self.fertigate, bg="green", fg="white")
        fertButton.place(x=150,y=300)
        waterButton = Button(tab2, text="Water", command=self.water, bg="blue", fg="white")
        waterButton.place(x=260,y=300)
        heatButton = Button(tab2, text="Heat", command=self.heat, bg="orange", fg="white")
        heatButton.place(x=350,y=300)
        
        tab_control.add(tab3, text='Error Status')
        quitButton = Button(tab3, text="Emergency Stop", command=self.client_exit, bg="red", fg="white")
        quitButton.place(x=430,y=5)

        tab_control.pack(expand=1, fill='both')
        
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
        
root = Tk()

root.geometry("600x500")

app = Window(root)
root.mainloop()  
