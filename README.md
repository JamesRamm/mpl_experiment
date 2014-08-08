mpl_experiment
==============

Working towards stylesheets...


Run `run.py` to generate examples of using a `Style` object rather than setting individual artists styles through get/set methods. 


This experiment provides a `Style` object and reimplements `Line2D` to use it. This is a very bare-bones implementation!

Create a `Line2D` instance and create a `Style` object seperately. Then add the style instance to the object:

  myLine = Line2D([0,1], [0,1])
  myStyle = Style()
  myStyle.color = '#484D7A'
  
  myLine.style = myStyle
  
If no style is specified, it reverts to the defaults in rcParams

`Style` holds information on colour, linewidth/style, transparency etc...

The idea is to handle the appearance (style) and data/logic of drawing seperately. 


This is just a proof of concept...there is much work to be done
