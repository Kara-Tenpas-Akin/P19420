#!/bin/sh

""":"
exec python $0 ${1+"$@"}
"""

# ---------------------------- HelloGraph.py ----------------------
# 
# This program demonstrates all methods available in the graph  
# part. Note that this program does not do anything useful;
# its purpose is only to demonstrate functionality.
#

from tkinter import *        # The Tk package
import Pmw                   # The Python MegaWidget package
import math                  # import the sin-function

master = Tk()                # build Tk-environment
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

g = Pmw.Blt.Graph(master)
g.pack(expand=1, fill='both')

color = ['red',   '#ff9900', 'blue', '#00cc00', 'black', 'grey']

########################### bar_create ###############################

# note: bars are not fully documented herein, but we add a short example on
#       how to use it here. You'll have to read the Tcl manual to
#       get the complete documentation for this package.

g.configure(barmode="overlap")
# "overlap" can be replaced by "stacked", "infront", "aligned", "overlap"
   
for c in range(ncurves):                   
    curvename = 'bar_sin(' + str(c) +'x)'   
    g.bar_create(curvename, 
                 xdata=tuple(vector_x),
                 barwidth=0.08,        
                 fg=color[c],          
                 ydata=tuple(vector_y[c]))


############################ line_create #############################

for c in range(ncurves):                
    curvename = 'sin(' + str(c) +'x)'    
    g.line_create(curvename,             
                  xdata=tuple(vector_x),  
                  ydata=tuple(vector_y[c]),
                  color=color[c],          
                  smooth='natural',        
                  linewidth=2,             
                  symbol='')               
   
############################### configure #############################

# The following example shows how to specify options to configure().

g.configure(title='Hello Graph',    # enter a title
            background='lightblue', # a bgcolor
            borderwidth=4,          # a thicker border
            relief="sunken",        # let it be sunken
            cursor="arrow")         # use arrow rather than crosshair.



################################## extents ############################
def showExtents():
    print("extents:")
    print ("leftmargin: ",   g.extents("leftmargin"  ))
    print ("rightmargin: ",  g.extents("rightmargin" ))
    print ("topmargin: ",    g.extents("topmargin"   ))
    print ("bottommargin: ", g.extents("bottommargin"))
    print ("plotwidth: ",    g.extents("plotwidth"   ))
    print ("plotheight: ",   g.extents("plotheight"  ))

################################# transform ############################
def showTransform():
    print ("screen coordinate (0,0) has axis coordinate: ", g.invtransform(0, 0))

################################# transform ############################
def showInvtransform():
    print ("axis coordinate (0,0) has screen coordinate: ", g.transform(0, 0))

################################## inside ##############################
def showInside():
    print ("screen coordinate (100,100) is "),
    if g.inside(100, 100):
        print ("inside "),
    else:
        print ("outside "),
        
    print ("the plotarea.")
    
################################### snap ################################
def showSnap():
    img = PhotoImage(name="image", master=master)
    g.snap(img)           # take snapshot
    img.write("file.ppm")  # and save it to file.
    print ("Snapshot taken an written to file: file.ppm")


# make row of buttons
buttons = Pmw.ButtonBox(master, labelpos='n', label_text='Options')
buttons.pack(fill='y', expand=1, padx=10, pady=10)

buttons.add('Extents',      command=showExtents)
buttons.add('Transform',    command=showTransform)
buttons.add('InvTransform', command=showInvtransform)
buttons.add('Inside',       command=showInside)
buttons.add('Snap',         command=showSnap)
buttons.add('Quit',         command=master.quit)

master.mainloop()


