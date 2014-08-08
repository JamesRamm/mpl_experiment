"""
 Experimenting with de-coupled style objects. 
 A 'Style' class is given in lines_style.py, along with a reimplementation of Line2D to show how it could be used.

 I.E the 'style' is created independently of the artist and is only added to the artist as a property.

 IMO this has various benefits:

 - This would allow 'style' objects to be easily generated from another source (such as a stylesheet...).
 A visitor algorithm could then be used to apply the style to the relevant artist

 - Artists no longer need to have many get/set methods. The 'Style' class can be expanded to include as many properties
 as needed and for artists that don't use x property, the draw method simply ignores it...

 - Makes the OO API much simpler and easy to use (IMO).
 
"""


from lines_style import Style, Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
import os
outputFolder = "C:\\"

# Setup the figure and axes
fig = Figure()
canvas = FigureCanvasAgg(fig)

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])


# Create a line object 
xdata = np.linspace(0, 2*np.pi, 100)
ydata = np.sin(xdata)

# Set the limits. Adding an artist to the axes manually doesn't update the limits...
ax.set_xlim(min(xdata)-0.2, max(xdata)+0.2) # Be a bit generous to see any changes we make to the capstyle...
ax.set_ylim(min(ydata)-0.2, max(ydata)+0.2) 

ln = Line2D(xdata, ydata)

# Add to the axis
ax.add_line(ln)

# Save this using the default style
canvas.print_png(os.path.join(outputFolder, "defaultStyle.png"))

# Make a style object and customise
style = Style()

style.color = '#484D7A' # A nice blue
style.alpha = 0.7
style.linewidth = 3.2 # Quite fat!
style.capstyle = 'round'
style.snap = False
style.linestyle = "dashed"

# We could do the same thing with a dictionary:
styleDict = {'color': '#484D7A',
           'alpha': 0.7,
           'linewidth': 3.2}
altStyle = Style.from_dict(styleDict)



# Apply the style object to the artist
ln.style = style

# save the result
canvas.print_png(os.path.join(outputFolder, "customStyle.png"))



