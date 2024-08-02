from __future__ import annotations
from typing import Optional

from schemdraw.elements import Element, Wire
from schemdraw.segments import SegmentPoly, SegmentText, Segment
from schemdraw.pictorial import INCH, PINSPACING, MILLIMETER


HOUSING_COLOR = '#333'  # Color of ICs, Diodes, etc.
LEAD_COLOR = '#A0A0A0'  # Color of leads/metal
NO_LW = 1e-6


class PrototypeBoard(Element):
    '''
    Protype board used for the High-Speed electronics practicum.

    Args:

    '''
    _element_defaults = {
        'color': '#DDD',  # Border
        'fill': '#964B00',
        'shadow_color': '#E5E5E5',
        'substrate_color': '#964B00',
        'metal_color': '#FFD700',
        'text_color': '#000000',
    }

    def __init__(self,
                 show_text: bool = True,
                 **kwargs):
        super().__init__(**kwargs)

        inner_radius = .02
        outer_radius = .1
        via_radius = .012
        shadow_color = self.params.get('shadow_color')
        substrate_color = self.params.get('substrate_color')
        metal_color = self.params.get('metal_color')
        text_color = self.params.get('text_color')

        def hole(x, y):
            self.segments.append(SegmentPoly(((x-outer_radius, y+outer_radius), (x+outer_radius, y+outer_radius),
                                              (x+outer_radius, y-outer_radius), (x-outer_radius, y-outer_radius)),
                                             fill=True, color=metal_color))
            self.segments.append(SegmentPoly(((x-inner_radius, y-inner_radius), (x-inner_radius, y+inner_radius),
                                              (x+inner_radius, y+inner_radius), (x+inner_radius, y-inner_radius)),
                                             fill=True, color=HOUSING_COLOR))

        def via(x, y):
            self.segments.append(SegmentPoly(((x-via_radius, y-via_radius), (x-via_radius, y+via_radius),
                                              (x+via_radius, y+via_radius), (x+via_radius, y-via_radius)),
                                             fill=True, color=HOUSING_COLOR))

        nrows = 16
        ncols = 16

        # Dimensionss from breadboard spec sheets
        grid_iso = (PINSPACING - 2*outer_radius)  # grid isolation
        strip_w = .2 * INCH  # ground boundary strip is 0.5 inch
        width = (ncols - 1)*PINSPACING + 2 * (PINSPACING - 2 *
                                              outer_radius) + 2 * outer_radius + 2*strip_w  # Total width
        height = (nrows - 1)*PINSPACING + 2 * (PINSPACING - 2 *
                                               outer_radius) + 2 * outer_radius + 2*strip_w  # Total height
        # width = (ncols + 1) * PINSPACING + 2*strip_w
        # height = (nrows + 1) * PINSPACING + 2*strip_w
        top = strip_w + (PINSPACING - 2*outer_radius) + outer_radius
        left = -strip_w - (PINSPACING - 2*outer_radius) - outer_radius
        right = left+width

        self.segments.append(
            SegmentPoly(((left, top), (right, top),
                         (right, top-height), (left, top-height)), fill=True, color=substrate_color))

        # Draw Ground boundary
        sma_iso = grid_iso*2  # isolation distance for SMA connector
        sma_width = 2*outer_radius
        # Start with SMA connections at top and bottom
        x_center = left + width / 2
        y1 = -2*PINSPACING
        y2 = -13*PINSPACING

        for y in [top, top - height + strip_w]:  # top and bottom sma connectors
            self.segments.append(SegmentPoly(((x_center - sma_width/2, y), (x_center + sma_width/2, y),
                                              (x_center + sma_width/2, y - strip_w), (x_center - sma_width/2, y - strip_w)),
                                             fill=True, color=metal_color))

        for x in (left, left + width - strip_w):  # left and right
            for y in (y1, y2):
                self.segments.append(SegmentPoly(((x, y + sma_width/2), (x + strip_w, y + sma_width/2),
                                                  (x + strip_w, y - sma_width/2), (x, y - sma_width/2)),
                                                 fill=True, color=metal_color))

            self.segments.append(SegmentPoly(((x, y1 - sma_width/2 - sma_iso),
                                              (x + strip_w, y1 -
                                               sma_width/2 - sma_iso),
                                              (x + strip_w, y2 +
                                               sma_width/2 + sma_iso),
                                              (x, y2 + sma_width/2 + sma_iso)),
                                             fill=True, color=metal_color))

        self.segments.append(SegmentPoly(((left, top), (x_center - sma_width/2 - sma_iso, top), (x_center - sma_width/2 - sma_iso, top - strip_w),
                                          (left + strip_w, top - strip_w), (left +
                                                                            strip_w, y1 + sma_width/2 + sma_iso),
                                          (left, y1 + sma_width/2 + sma_iso)),
                                         fill=True, color=metal_color))

        self.segments.append(SegmentPoly(((left, top - height), (x_center - sma_width/2 - sma_iso, top - height),
                                          (x_center - sma_width/2 -
                                           sma_iso, top - height + strip_w),
                                          (left + strip_w, top - height + strip_w), (left +
                                                                                     strip_w, y2 - sma_width/2 - sma_iso),
                                          (left, y2 - sma_width/2 - sma_iso)),
                                         fill=True, color=metal_color))

        self.segments.append(SegmentPoly(((right, top), (x_center + sma_width/2 + sma_iso, top), (x_center + sma_width/2 + sma_iso, top - strip_w),
                                          (right - strip_w, top - strip_w), (right -
                                                                             strip_w, y1 + sma_width/2 + sma_iso),
                                          (right, y1 + sma_width/2 + sma_iso)),
                                         fill=True, color=metal_color))

        self.segments.append(SegmentPoly(((right, top - height), (x_center + sma_width/2 + sma_iso, top - height),
                                          (x_center + sma_width/2 +
                                           sma_iso, top - height + strip_w),
                                          (right - strip_w, top - height + strip_w), (right -
                                                                                      strip_w, y2 - sma_width/2 - sma_iso),
                                          (right, y2 - sma_width/2 - sma_iso)),
                                         fill=True, color=metal_color))

        # add SMA anchors
        self.anchors['sma_top'] = (x_center, top)
        self.anchors['sma_bot'] = (x_center, top-height)
        self.anchors['sma_left_top'] = (left, y1)
        self.anchors['sma_left_bot'] = (left, y2)
        self.anchors['sma_right_top'] = (right, y1)
        self.anchors['sma_right_bot'] = (right, y2)

        # add solder anchors
        self.anchors['sma_top_solder'] = (x_center, top - strip_w)
        self.anchors['sma_bot_solder'] = (x_center, top - height + strip_w)
        self.anchors['sma_left_top_solder'] = (left + strip_w, y1)
        self.anchors['sma_left_bot_solder'] = (left + strip_w, y2)
        self.anchors['sma_right_top_solder'] = (right - strip_w, y1)
        self.anchors['sma_right_bot_solder'] = (right - strip_w, y2)

        # Inner Rows
        x = 0
        y = 0
        for col in range(ncols):
            colname = chr(ord('A')+col)
            if show_text:
                self.segments.append(SegmentText((x+col*PINSPACING, y+PINSPACING), colname,
                                                 fontsize=8, rotation_global=False, align=('center', 'center'),
                                                 color=text_color, zorder=1))
            for row in range(nrows):
                xy = x+col*PINSPACING, y-row*PINSPACING
                hole(*xy)
                self.anchors[f'{colname}{row+1}'] = xy

        # Number Labels
        if show_text:
            for row in range(0, nrows):
                self.segments.append(SegmentText((x-PINSPACING, y-row*PINSPACING-.04), str(row+1), fontsize=8,
                                                 rotation_global=False, align=('center', 'bottom'), color=text_color, zorder=1))


class SMA(Element):
    _element_defaults = {
        'theta': 0,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pin_color = '#ffbf00'
        top_color = '#bf9b30'
        width = 0.5
        left = -width/2
        right = width/2
        top = 1
        pin_width = 0.18
        pin_length = 0.18*INCH
        ground_pin_length = 0.15*INCH
        top_length = 0.2
        screw_length = 1
        screw_width = 0.45
        strip_w = 0.2*INCH
        sma_iso = 0.3

        # top
        self.segments.append(SegmentPoly(((-3*pin_width/2 - sma_iso, 0), (3*pin_width/2 + sma_iso, 0),
                                          (3*pin_width/2 + sma_iso, top_length), (-3*pin_width/2 - sma_iso, top_length)),
                                         fill=True, color=top_color, lw=NO_LW))
        # center pin
        self.segments.append(SegmentPoly(((-pin_width/2, 0), (-pin_width/2, -pin_length), (pin_width/2, -pin_length), (pin_width/2, 0)),
                                         fill=True, color=pin_color, lw=NO_LW))

        # ground pins
        for x in [-3*pin_width/2 - sma_iso, pin_width/2 + sma_iso]:
            self.segments.append(SegmentPoly(((x, 0), (x + pin_width, 0), (x + pin_width, -ground_pin_length), (x, -ground_pin_length)),
                                             fill=True, color=pin_color, lw=NO_LW))

        # screw part
        self.segments.append(SegmentPoly(((-screw_width/2, top_length), (screw_width/2, top_length),
                                          (screw_width/2, top_length+screw_length), (-screw_width/2, top_length+screw_length)),
                                         fill=True, color=pin_color, lw=NO_LW))

        for i in range(6):
            self.segments.append(Segment(((-screw_width/2*1.1, top_length + screw_length - 0.1 - 0.1*i), (screw_width/2*1.1, top_length + screw_length - 0.08 - 0.1*i)),
                                         color=top_color))


class SOT23(Element):
    _element_defaults = {
        'theta': 0,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # lead 1
        self.segments.append(SegmentPoly(((-0.2*MILLIMETER, 0.2*MILLIMETER), (-0.2*MILLIMETER, -0.2*MILLIMETER),
                                          (0.4*MILLIMETER, -0.2*MILLIMETER), (0.4*MILLIMETER, 0.2*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # lead 2
        self.segments.append(SegmentPoly(((-0.2*MILLIMETER, -1.7*MILLIMETER), (-0.2*MILLIMETER, -2.1*MILLIMETER),
                                          (0.4*MILLIMETER, -2.1*MILLIMETER), (0.4*MILLIMETER, -1.7*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # lead 3
        self.segments.append(SegmentPoly(((1.8*MILLIMETER, -0.75*MILLIMETER), (1.8*MILLIMETER, -1.15*MILLIMETER),
                                          (2.4*MILLIMETER, -1.15*MILLIMETER), (2.4*MILLIMETER, -0.75*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))
        # package
        self.segments.append(SegmentPoly(((0.4*MILLIMETER, 0.7*MILLIMETER), (0.4*MILLIMETER, -2.7*MILLIMETER),
                                          (1.8*MILLIMETER, -2.7*MILLIMETER), (1.8*MILLIMETER, 0.7*MILLIMETER)),
                                         fill=True, color=HOUSING_COLOR, lw=NO_LW))

        self.anchors['1'] = (0, 0)
        self.anchors['2'] = (0, -1.9*MILLIMETER)
        self.anchors['3'] = (2.2*MILLIMETER, -0.95*MILLIMETER)


class CapacitorSMD(Element):
    ''' 
    0603 imperial SMD capacitor
    '''
    _element_defaults = {
        'theta': 0,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        substrate_color = '#B59667'

        # lead 1
        self.segments.append(SegmentPoly(((-0.2*MILLIMETER, 0.4*MILLIMETER), (-0.2*MILLIMETER, -0.4*MILLIMETER),
                                          (0.2*MILLIMETER, -0.4*MILLIMETER), (0.2*MILLIMETER, 0.4*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # lead 2
        self.segments.append(SegmentPoly(((1*MILLIMETER, 0.4*MILLIMETER), (1*MILLIMETER, -0.4*MILLIMETER),
                                          (1.4*MILLIMETER, -0.4*MILLIMETER), (1.4*MILLIMETER, 0.4*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # substrate
        self.segments.append(SegmentPoly(((0.2*MILLIMETER, 0.4*MILLIMETER), (0.2*MILLIMETER, -0.4*MILLIMETER),
                                          (1*MILLIMETER, -0.4*MILLIMETER), (1*MILLIMETER, 0.4*MILLIMETER)),
                                         fill=True, color=substrate_color, lw=NO_LW))


class B4F(Element):
    ''' 
    Balun
    '''
    _element_defaults = {
        'theta': 0,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # lead 1
        self.segments.append(SegmentPoly(((0*MILLIMETER, 0*MILLIMETER), (0*MILLIMETER, 0.7*MILLIMETER),
                                          (1.4*MILLIMETER, 0.7*MILLIMETER), (1.4*MILLIMETER, 0*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # lead 2
        self.segments.append(SegmentPoly(((0*MILLIMETER, 1.5*MILLIMETER), (0*MILLIMETER, 2.2*MILLIMETER),
                                          (1.4*MILLIMETER, 2.2*MILLIMETER), (1.4*MILLIMETER, 1.5*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # lead 3
        self.segments.append(SegmentPoly(((0*MILLIMETER, 3*MILLIMETER), (0*MILLIMETER, 3.7*MILLIMETER),
                                          (1.4*MILLIMETER, 3.7*MILLIMETER), (1.4*MILLIMETER, 3*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # core
        self.segments.append(SegmentPoly(((1.4*MILLIMETER, -0.35*MILLIMETER), (1.4*MILLIMETER, 4.05*MILLIMETER),
                                          (4.1*MILLIMETER, 4.05*MILLIMETER), (4.1*MILLIMETER, -0.35*MILLIMETER)),
                                         fill=True, color=HOUSING_COLOR, lw=NO_LW))

        # lead 6
        self.segments.append(SegmentPoly(((4.1*MILLIMETER, 0*MILLIMETER), (4.1*MILLIMETER, 0.7*MILLIMETER),
                                          (5.5*MILLIMETER, 0.7*MILLIMETER), (5.5*MILLIMETER, 0*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))

        # lead 4
        self.segments.append(SegmentPoly(((4.1*MILLIMETER, 3*MILLIMETER), (4.1*MILLIMETER, 3.7*MILLIMETER),
                                          (5.5*MILLIMETER, 3.7*MILLIMETER), (5.5*MILLIMETER, 3*MILLIMETER)),
                                         fill=True, color=LEAD_COLOR, lw=NO_LW))


class Solder(Wire):
    def __init__(self, shape: str = '-', k: float = 1, arrow: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._userparams['shape'] = shape
        self._userparams['k'] = k
        self._userparams.setdefault('to', (3, -2))
        self._userparams['color'] = '#808080'
        self._userparams['lw'] = 7
