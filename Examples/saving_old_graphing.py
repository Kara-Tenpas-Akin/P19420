# Graphs
color = ['red', '#ff9900', 'blue', '#00cc00', 'black', 'grey']

#First line              
curvename = str('Inside Temp')
list_x = comm.getGraphData()
list_y = comm.getGraphData()
g.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[0],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
curvename = str('Outside Temp')
list_x = comm.getGraphData()
list_y = comm.getGraphData()
g.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[2],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
curvename = str('Row 1')
list_x = comm.getGraphData()
list_y = comm.getGraphData()
gg.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[3],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
curvename = str('Row 2')
list_x = comm.getGraphData()
list_y = comm.getGraphData()
gg.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[4],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
curvename = str('Row 3')
list_x = comm.getGraphData()
list_y = comm.getGraphData()
gg.line_create(curvename,             
                        xdata=tuple(list_x),  
                        ydata=tuple(list_y),
                        color=color[5],          
                        smooth='natural',        
                        linewidth=2,             
                        symbol='')
