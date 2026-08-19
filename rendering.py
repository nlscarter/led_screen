from drawing import draw_custom_char, draw_custom_string, draw_horizontal_line
from fonts.custom_font import LOGO_DATA, FLAG_DATA, font_4x7, class_lines, font_5x9


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
        x_lengths = [13,10,11,47]
        draw_custom_string(canvas, o_mgr, self.pos, start_x=sum(x_lengths[:1])-2, start_y=y_pos, font_data=font_5x9, right_justify=True)
        draw_custom_string(canvas, o_mgr, self.num, start_x=sum(x_lengths[:1]), start_y=y_pos - 2, font_data=font_4x7)
        draw_custom_char(canvas, o_mgr, self.status, start_x=sum(x_lengths[:2]), start_y=y_pos, font_data=LOGO_DATA)
        draw_custom_string(canvas, o_mgr, self.name, start_x=sum(x_lengths[:3]), start_y=y_pos - 2, font_data=font_4x7)
        draw_custom_char(canvas, o_mgr, self.country, start_x=sum(x_lengths[:4]), start_y=y_pos, font_data=FLAG_DATA)

        draw_horizontal_line(canvas, o_mgr, start_x=sum(x_lengths[:1]), start_y=y_pos, length=x_lengths[1]-1, color_idx=self.category)
        draw_horizontal_line(canvas, o_mgr, start_x=sum(x_lengths[:3]), start_y=y_pos, length=45, color_idx=11)

        return 10

class RenderTitle:
    """Heading of page"""

    def __init__(self):
        a=0

    def render(self, canvas, o_mgr, y_pos):
        draw_custom_char(canvas, o_mgr, "ROLEX", start_x=2, start_y=y_pos, font_data=LOGO_DATA)
        return 9

rows_data = [
        RenderTitle(),
        RenderRow(status="FERRARI", country="GBR", category=1, num="12", pos="1", name="S.Teve"),
        RenderRow(status="PORSCHE", country="JAP", category=4, num="56", pos="8", name="D.Ave"),
        RenderRow(status="BMW", country="ITY", category=2, num="007", pos="17", name="S.Buemi"),
        RenderRow(status="COLOUR1", country="JAP", category=1, num="04", pos="23", name="N.Carter"),
    ]