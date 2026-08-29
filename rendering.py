import datetime
from zoneinfo import ZoneInfo

from drawing import horizontal_line, class_line, small_font_string, flag, draw_logo, large_font_string

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
        x_frames = [13,1,10,11,46]
        large_font_string(canvas, o_mgr, self.pos, x_frames=x_frames, x_frame=0, start_y=y_pos - 1, justify='center')
        class_line(canvas, o_mgr, self.category, start_x=sum(x_frames[:1]) - 1, start_y=y_pos)
        horizontal_line(canvas, o_mgr, start_x=sum(x_frames[:1]), start_y=y_pos, length=x_frames[2], color_idx=self.category)
        small_font_string(canvas, o_mgr, self.num, x_gaps=x_frames, x_frame=2, start_y=y_pos - 2, colour=8)
        draw_logo(canvas, o_mgr, self.status, start_x=sum(x_frames[:3]), start_y=y_pos)
        small_font_string(canvas, o_mgr, self.name, x_gaps=x_frames, x_frame=4, start_y=y_pos - 2)
        flag(canvas, o_mgr, self.country, start_x=sum(x_frames[:5]), start_y=y_pos)

        horizontal_line(canvas, o_mgr, start_x=sum(x_frames[:4]), start_y=y_pos, length=x_frames[-1] - 1, color_idx=11)
        return 10

class RenderTitle:
    """Heading of page"""
    def __init__(self, flag, lap):
        self.flag = flag
        tz = ZoneInfo("GMT")
        ft = "%H:%M:%S"
        time_now = datetime.datetime.now(tz=tz).strftime(ft)
        self.time_now = time_now
        self.lap = lap
        self.lap_string = f'Lap:{lap}'

    def render(self, canvas, o_mgr, y_pos):
        x_lengths = [22, 43, 33]
        draw_logo(canvas, o_mgr, "ROLEX", start_x=0, start_y=y_pos)
        small_font_string(canvas, o_mgr, self.time_now, x_gaps=x_lengths, x_frame=1, start_y=y_pos - 1, colour=0xB, justify='center')
        small_font_string(canvas, o_mgr, self.lap_string, x_gaps=x_lengths, x_frame=2, start_y=y_pos - 1, colour=0xD, justify='right')

        return 9

rows_data = [
        RenderTitle(flag='fcy', lap=358),
        RenderRow(status="FERRARI", country="GBR", category=1, num="12", pos="1", name="abcdefghi"),
        RenderRow(status="PORSCHE", country="JAP", category=4, num="56", pos="8", name="jklmnopqr"),
        RenderRow(status="BMW", country="ITY", category=2, num="007", pos="14",   name="stuvwxyz!"),
        RenderRow(status="COLOUR1", country="JAP", category=1, num="04", pos="23", name="  ;+=;"),
    ]