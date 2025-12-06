from typing import Literal

class Parameters:
    HSTEP = 13
    VSTEP = 18
    CURSOR_X = 13
    CURSOR_Y = 18
    SCROLLSTEP = 100
    HEIGHT = 800
    WIDTH = 600
    SCROLL = 0
    CHAR_SIZE = 12
    STYLE: Literal["italic", "roman"] = "roman"
    WEIGHT: Literal["normal", "bold"] = "normal"
