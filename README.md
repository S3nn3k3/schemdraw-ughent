# schemdraw-ughent
Schemdraw extension which contains (pictorial) elements specific for Ghent University courses. More specific High Speed Electronics.

This library is an extension of [schemdraw](https://schemdraw.readthedocs.io/en/latest/index.html). Read their documentation in order to get familiar with it. After reading this documentation you can you further with this library.

The basic usage (relevant for the High Speed Electronics course) is as follows:

```python
from schemdraw import Drawing
from schemdraw.elements import Wire
from schemdraw.pictorial import MILLIMETER
from schemdraw_ughent.hse import SOT23, PrototypeBoard, SMA, Solder, CapacitorSMD, B4F

with Drawing() as d:
    bb = PrototypeBoard(show_text=True)

    SMA().at(bb.sma_top).label("Test")
    SMA(theta=-90).at(bb.sma_right_top).label("Test", loc="bot")
    SMA(theta=-90).at(bb.sma_right_bot)
    SMA(theta=180).at(bb.sma_bot)
    SMA(theta=90).at(bb.sma_left_top)
    SMA(theta=90).at(bb.sma_left_bot)

    Solder().at(bb.sma_top_solder).to(bb.I1)
    Solder("|-").at(bb.I1).to(bb.sma_right_bot_solder)

    SOT23(theta=15).at(bb.C5, dx=0.2*MILLIMETER, dy=-0.3*MILLIMETER)
    B4F(theta=-42).at(bb.D9, dx=-0.5*MILLIMETER, dy=0.5*MILLIMETER)

    B4F().at(bb.D14, dy=0.6*MILLIMETER)

    CapacitorSMD().at(bb.F5, dx=0.7*MILLIMETER)
```
