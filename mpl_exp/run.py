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

from __future__ import print_function

from lines_style import Style, Line2D, Text, Font # These are our reimplemented artists
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
import os

outputFolder = "/home/james/"

# Setup the figure and axes
fig = Figure()
canvas = FigureCanvasAgg(fig)

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

#######First experiment: Create a line and add a custom 'style' #############
# Create a line object 
xdata = np.linspace(0, 2*np.pi, 100)
ydata = np.sin(xdata)

ln = Line2D(xdata, ydata)

# Set the limits. Adding an artist to the axes manually doesn't update the limits so we must do this...
ax.set_xlim(min(xdata)-0.2, max(xdata)+0.2) # Be a bit generous to see any changes we make to the capstyle...
ax.set_ylim(min(ydata)-0.2, max(ydata)+0.2) 

# Add to the axis
ax.add_line(ln)

# If we don't set the style property to a 'Style' object, it simply gets defaults from rcParams. Let's test:
canvas.print_png(os.path.join(outputFolder, "defaultStyle.png"))

# Now lets make a 'Style' object, change the settings we want and set the style property of our line to this object
style = Style()

style.color = 'black' # A nice blue
style.alpha = 0.9
style.linewidth = 3.2 # Quite fat!
style.capstyle = 'round'
style.snap = False
style.linestyle = "dashed"

# We could initialise the style object with a dictionary, using the from_dict class method:
styleDict = {'color': '#484D7A',
           'alpha': 0.9,
           'linewidth': 3.2}
altStyle = Style.from_dict(styleDict)

# Apply the style object to the artist
ln.style = style

# save the result
canvas.print_png(os.path.join(outputFolder, "customStyle.png"))

# If we change the original style object, the change is reflected in all artists that reference it:
style.alpha = 0.1
print(ln.style.alpha)

##### Second experiment: Text #####
#Get rid of the line and try some text
ax.lines = []

# The 'style' of Text is controlled by two objects: Style and Font. 
# Make a Font object that we will use for all text
fnt = Font("Ubuntu", size = 14)

# make a text object, reusing the style object we previously created...because we are lazy!
txt = Text(0.5, 0.5, "Hello", style = style, fontproperties = fnt)

# make another text object and lets use a different style, but the same font. This time, use the from_dict method to generate the style
txt2 = Text(0.1, 0.7, "Fun with styles")
txt2.style = Style.from_dict({"color": '#E98300'})
txt2.font = fnt

#Because axes has no add_text method, we need to set its figure manually
txt.set_figure(fig)
txt.set_axes(ax)
txt.set_transform(ax.transData)
txt2.set_figure(fig)
txt2.set_axes(ax)
txt2.set_transform(ax.transData)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

ax.texts.extend([txt, txt2])
canvas.print_png(os.path.join(outputFolder, "customTextStyle.png"))

# Unfortunatly, changes to the font object are not reflected in associated artists because currently set_fontproperties (the MPL method which is called when we do txt.font = fnt) makes a copy
# of the object...
print(txt.font.size)
fnt.size = 22
print(txt.font.size)






