from matplotlib.backend_bases import GraphicsContextBase
from matplotlib.lines import Line2D as mLine2D
from matplotlib.text import Text as mText
from matplotlib.artist import allow_rasterization
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
import numpy as np

"""
 Note: GraphicsContextBase has a bug in get_linestyle where it requires the arguement 'style'. 
 This argument is not used and should be deleted. For the time being, I reimplemented get_linestyle
"""

class Font(FontProperties):
    """ Simple class to propertify FontProperties"""
    family = property(FontProperties.get_family, FontProperties.set_family)
    style = property(FontProperties.get_style, FontProperties.set_style)
    variant = property(FontProperties.get_variant, FontProperties.set_variant)
    weight = property(FontProperties.get_weight, FontProperties.set_weight)
    stretch = property(FontProperties.get_stretch, FontProperties.set_stretch)
    size = property(FontProperties.get_size, FontProperties.set_size)


class Style(GraphicsContextBase):

    _lineStyles = {
    '-':    'solid',
     '--':   'dashed',
    '-.':   'dashdot',
    ':':    'dotted'}

    def get_graylevel(self):
        'Just returns the foreground color'
        return self._rgb

    def get_linestyle(self):
        ' Only here because of a bug in MPL. just removing the unneeded arguement from the func...'
        return self._linestyle

    alpha = property(GraphicsContextBase.get_alpha, GraphicsContextBase.set_alpha)
    antialiased = property(GraphicsContextBase.get_antialiased, GraphicsContextBase.set_antialiased)
    capstyle = property(GraphicsContextBase.get_capstyle, GraphicsContextBase.set_capstyle)
    clip_rectangle = property(GraphicsContextBase.get_clip_rectangle, GraphicsContextBase.set_clip_rectangle)
    clip_path = property(GraphicsContextBase.get_clip_path, GraphicsContextBase.set_clip_path)
    graylevel = property(get_graylevel, GraphicsContextBase.set_graylevel)
    joinstyle = property(GraphicsContextBase.get_joinstyle, GraphicsContextBase.set_joinstyle)
    linewidth = property(GraphicsContextBase.get_linewidth, GraphicsContextBase.set_linewidth)
    linestyle = property(get_linestyle, GraphicsContextBase.set_linestyle)
    url = property(GraphicsContextBase.get_url, GraphicsContextBase.set_url)
    gid = property(GraphicsContextBase.get_gid, GraphicsContextBase.set_gid)
    snap = property(GraphicsContextBase.get_snap, GraphicsContextBase.set_snap)
    hatch = property(GraphicsContextBase.get_hatch, GraphicsContextBase.set_hatch)
   

    # Refactoring of set_dashes into two properties..
    @property
    def dash_offset(self):
        return self._dashes[0]
    @dash_offset.setter
    def dash_offset(self, value):
        self._dashes[0] = value

    @property
    def dashes(self):
        return self._dashes[1]

    @dashes.setter
    def dashes(self, value):
        if value is not None:
            dl = np.asarray(value)
            if np.any(dl <= 0.0):
                raise ValueError("All values in the dash list must be positive")

        self._dashed[1] = value

    #Color property is an alternative to 'set_foreground'. It does the same thing, but makes no allowances for providing a colour already in RGBA format..
    @property
    def color(self):
        return self._rgb
    @color.setter
    def color(self, value):
        self.set_foreground(value)

    # Defining 3 properties for sketch params
    @property
    def sketch_scale(self):
        return self._sketch[0]
    @sketch_scale.setter
    def sketch_scale(self, value):        
        self.set_sketch_params(scale = value)

    @property
    def sketch_length(self):
        return self._sketch[1]
    @sketch_length.setter
    def sketch_length(self, value):
        self.set_sketch_params(length = value)

    @property
    def sketch_randomness(self):
        return self._sketch[2]
    @sketch_randomness.setter
    def sketch_randomness(self, value):
        self.set_sketch_params(randomness = value)

    @classmethod
    def from_dict(cls, styleDict):
        """ Generate a style class from a dictionary """
        st = cls()
        for key, value in styleDict.iteritems():
            setattr(st, key, value)

        return st
    
def style_property(name = 'style', expected_type = Style):
    """ Property for style attributes. Performs type checking """
    storage_name = '_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)
    @prop.setter
    def prop(self, value):
        if isinstance(value, expected_type) or value is None:
            setattr(self, storage_name, value)
        else:
            raise TypeError('{} must be a {}'.format(name, expected_type))
         
    return prop

class Line2D(mLine2D):
    """ 
    Reimplementation of Line2D to support a 'style' property. This is not the full implementation.
    Support for markers is not in the draw method. (Another style property required?)
    """

    lineStyles = _lineStyles = {  # hidden names deprecated
    '-':    'solid',
    '--':   'dashed',
    '-.':   'dashdot',
    ':':    'dotted'
    }

    style = style_property()
    markerStyle = style_property('markerStyle')


    def __init__(self, xdata, ydata,
                 style = None, markerstyle = None,
                linewidth=None,  # all Nones default to rc
                linestyle=None,
                color=None,
                marker=None,
                markersize=None,
                markeredgewidth=None,
                markeredgecolor=None,
                markerfacecolor=None,
                markerfacecoloralt='none',
                fillstyle='full',
                antialiased=None,
                dash_capstyle=None,
                solid_capstyle=None,
                dash_joinstyle=None,
                solid_joinstyle=None,
                pickradius=5,
                drawstyle=None,
                markevery=None,
                **kwargs
                ):

        super(Line2D, self).__init__(xdata, ydata,
                linewidth,  # all Nones default to rc
                linestyle,
                color,
                marker,
                markersize,
                markeredgewidth,
                markeredgecolor,
                markerfacecolor,
                markerfacecoloralt,
                fillstyle,
                antialiased,
                dash_capstyle,
                solid_capstyle,
                dash_joinstyle,
                solid_joinstyle,
                pickradius,
                drawstyle,
                markevery,
                **kwargs
                )

        self.style = style
        self.markerStyle = markerstyle
    def _defaultStyle(self):

        self.style = Style()
        #antialiased
        self.style.antialiased = rcParams['lines.antialiased']
        #capstyle

        #linewidth
        self.style.linewidth = rcParams['lines.linewidth']
        #linestyle
        linestyle = rcParams['lines.linestyle']
        if linestyle in self.lineStyles.keys():
            self.style.linestyle = self.lineStyles[linestyle]
        elif linestyle in self.lineStyles.values():
            self.style.linestyle = linestyle

        if self.style.linestyle in ['dashed', 'dashdot', 'dotted']:
            self.style.capstyle = rcParams['lines.dash_capstyle']
            self.style.joinstyle = rcParams['lines.dash_joinstyle']
        else:
            self.style.capstyle = rcParams['lines.solid_capstyle']
            self.style.joinstyle = rcParams['lines.solid_joinstyle']

        self.style.snap = self.get_snap()
        

        #Color by getting a default color then calling _get_rgba_l_color and setting the set_forground method of Style
        self.style.color = rcParams['lines.color']
        

    @allow_rasterization
    def draw(self, renderer):
        """Reimplementation of the class 'draw' method to use a Style object. This is just a small 'proof of concept' - markers are not implemented"""
        if not self.get_visible():
            return

        if self._invalidy or self._invalidx:
            self.recache()
        self.ind_offset = 0  # Needed for contains() method.
        if self._subslice and self.axes:
            # Need to handle monotonically decreasing case also...
            x0, x1 = self.axes.get_xbound()
            i0, = self._x.searchsorted([x0], 'left')
            i1, = self._x.searchsorted([x1], 'right')
            subslice = slice(max(i0 - 1, 0), i1 + 1)
            self.ind_offset = subslice.start
            self._transform_path(subslice)

        transf_path = self._get_transformed_path()

        if self.get_path_effects():
            from matplotlib.patheffects import PathEffectRenderer
            renderer = PathEffectRenderer(self.get_path_effects(), renderer)

        renderer.open_group('line2d', self.get_gid())
        

        if self.style == None:
            self._defaultStyle()

        if self.style.clip_path is None and self.style.clip_rectangle is None:
            self._set_gc_clip(self.style)

        tpath, affine = transf_path.get_transformed_path_and_affine()
        if len(tpath.vertices):
            self._lineFunc = self.draw_path
            funcname = self.drawStyles.get(self._drawstyle, '_draw_lines')
            drawFunc = getattr(self, funcname)
            drawFunc(renderer, self.style, tpath, affine.frozen())

        self.style.restore() #Unsure as to whether this is even applicable
        renderer.close_group('line2d')

    def draw_path(self, renderer, style, path, trans):
        """
        a monkey patch for now , but ideally the 'drawFunc' (got from drawstyle) would just be reimplemented to call rendered.draw_path.

        this is because the 'linefunc' is not particularly necessary to set the line style - we can do that in 'defaultStyle' function if it doesnt exist
        """
        renderer.draw_path(style, path, trans)

class Text(mText):

    font = property(mText.get_fontproperties, mText.set_fontproperties)
    style = style_property()
    text = property(mText.get_text, mText.set_text)
    gid = property(mText.get_gid, mText.set_gid)
    transform = property(mText.get_transform, mText.set_transform)

    def __init__(self,
                x=0, y=0, text='',
                style = None,
                color=None,           # defaults to rc params
                verticalalignment='baseline',
                horizontalalignment='left',
                multialignment=None,
                fontproperties=None,  # defaults to FontProperties()
                rotation=None,
                linespacing=None,
                rotation_mode=None,
                **kwargs
                ):

        super(Text, self).__init__(x, y, text,
                color,           # defaults to rc params
                verticalalignment,
                horizontalalignment,
                multialignment,
                fontproperties,  # defaults to FontProperties()
                rotation,
                linespacing,
                rotation_mode,
                **kwargs)

        self.style = style

    def _defaultStyle(self):

        self.style = Style()
        #antialiased
        self.style.antialiased = rcParams['lines.antialiased']
        #capstyle

        #linewidth
        self.style.linewidth = rcParams['lines.linewidth']
        #linestyle
        linestyle = rcParams['lines.linestyle']
        if linestyle in self.lineStyles.keys():
            self.style.linestyle = self.lineStyles[linestyle]
        elif linestyle in self.lineStyles.values():
            self.style.linestyle = linestyle

        if self.style.linestyle in ['dashed', 'dashdot', 'dotted']:
            self.style.capstyle = rcParams['lines.dash_capstyle']
            self.style.joinstyle = rcParams['lines.dash_joinstyle']
        else:
            self.style.capstyle = rcParams['lines.solid_capstyle']
            self.style.joinstyle = rcParams['lines.solid_joinstyle']

        self.style.snap = self.get_snap()

    @allow_rasterization
    def draw(self, renderer):
        """
        Draws the :class:`Text` object to the given *renderer*.
        """
        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible():
            return
        if self.text.strip() == '':
            return

        renderer.open_group('text', self.gid)

        bbox, info, descent = self._get_layout(renderer)
        trans = self.transform

        # don't use self.get_position here, which refers to text position
        # in Text, and dash position in TextWithDash:
        posx = float(self.convert_xunits(self._x))
        posy = float(self.convert_yunits(self._y))

        posx, posy = trans.transform_point((posx, posy))
        canvasw, canvash = renderer.get_canvas_width_height()

        # draw the FancyBboxPatch
        if self._bbox_patch:
            self._draw_bbox(renderer, posx, posy)

        if self.style == None:
            self._defaultStyle()

        if self.style.clip_path is None and self.style.clip_rectangle is None:
            self._set_gc_clip(self.style)

        if self._bbox:
            bbox_artist(self, renderer, self._bbox)
        angle = self.get_rotation()

        for line, wh, x, y in info:
            if not np.isfinite(x) or not np.isfinite(y):
                continue

            mtext = self if len(info) == 1 else None
            x = x + posx
            y = y + posy
            if renderer.flipy():
                y = canvash - y
            clean_line, ismath = self.is_math_text(line)

            if self.get_path_effects():
                from matplotlib.patheffects import PathEffectRenderer
                renderer = PathEffectRenderer(self.get_path_effects(),
                                              renderer)

            if rcParams['text.usetex']:
                renderer.draw_tex(self.style, x, y, clean_line,
                                  self.font, angle, mtext=mtext)
            else:
                renderer.draw_text(self.style, x, y, clean_line,
                                   self.font, angle,
                                   ismath=ismath, mtext=mtext)

        self.style.restore()
        renderer.close_group('text')
	
