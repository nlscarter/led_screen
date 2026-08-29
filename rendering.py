from matplotlib.pyplot import draw_all

from drawing import _draw_custom_char, _draw_custom_string, horizontal_line, class_line, \
    small_font_string, flag, draw_logo, large_font_string
from fonts.custom_font import LOGO_DATA, FLAG_DATA, font_4x7, font_5x9, class_vertlines


class RenderRow:
    """Heading of page"""

    def __init__(self, status, country, category, num, pos, name):
        self.status = status
        self.country = country
        self.category = category
        self.num = num
        self.pos = pos
        self.name = name


    def render(self, canvas, o_mgr, y_pos):
        x_lengths = [13,1,10,11,46]
        large_font_string(canvas, o_mgr, self.pos, x_gaps=x_lengths, x_pos=0, start_y=y_pos - 1,justify='center')
        class_line(canvas, o_mgr, self.category, start_x=sum(x_lengths[:1]) - 1, start_y=y_pos)
        horizontal_line(canvas, o_mgr, start_x=sum(x_lengths[:1]), start_y=y_pos, length=x_lengths[2], color_idx=self.category)
        small_font_string(canvas, o_mgr, self.num, x_gaps=x_lengths, x_pos=2, start_y=y_pos - 2, colour=8)
        draw_logo(canvas, o_mgr, self.status, start_x=sum(x_lengths[:3]), start_y=y_pos)
        small_font_string(canvas, o_mgr, self.name, x_gaps=x_lengths, x_pos=4, start_y=y_pos - 2)
        flag(canvas, o_mgr, self.country, start_x=sum(x_lengths[:5]), start_y=y_pos)

        horizontal_line(canvas, o_mgr, start_x=sum(x_lengths[:4]), start_y=y_pos, length=x_lengths[-1] - 1, color_idx=11)
        return 10

class RenderTitle:
    """Heading of page"""

    def __init__(self):
        a=0

    def render(self, canvas, o_mgr, y_pos):
        x_lengths = [25, 40]
        draw_logo(canvas, o_mgr, "ROLEX", start_x=2, start_y=y_pos)
        small_font_string(canvas, o_mgr, "12:34:56", x_gaps=x_lengths, x_pos=1, start_y=y_pos-1, colour=0xB, justify='right')

        return 9

rows_data = [
        RenderTitle(),
        RenderRow(status="FERRARI", country="GBR", category=1, num="12", pos="1", name="abcdefghi"),
        RenderRow(status="PORSCHE", country="JAP", category=4, num="56", pos="8", name="jklmnopqr"),
        RenderRow(status="BMW", country="ITY", category=2, num="007", pos="17",   name="stuvwxyz!"),
        RenderRow(status="COLOUR1", country="JAP", category=1, num="04", pos="23", name="  ;+=;"),
    ]