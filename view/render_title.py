import datetime
from zoneinfo import ZoneInfo

from engine.drawing import draw_logo, small_font_string


class RenderTitle:
    """Heading of page"""
    def __init__(self, flag, session):

        results = session.results()
        self.flag = flag
        tz = ZoneInfo("UTC")
        ft = "%H:%M:%S"
        time_now = datetime.datetime.now(tz=tz).strftime(ft)
        self.time_now = time_now
        self.lap = results['laps_completed'].iloc[0]
        self.lap_string = f'Lap:{self.lap}'

    def render(self, canvas, o_mgr, y_pos):
        x_lengths = [22, 43, 33]
        draw_logo(canvas, o_mgr, self.flag, start_x=0, start_y=y_pos)
        small_font_string(canvas, o_mgr, self.time_now, x_gaps=x_lengths, x_frame=1, start_y=y_pos - 1, colour=0xB, justify='center')
        small_font_string(canvas, o_mgr, self.lap_string, x_gaps=x_lengths, x_frame=2, start_y=y_pos - 1, colour=0xD, justify='right')
        return 9
