import datetime

from engine.drawing import draw_logo, small_font_string


class RenderTitle:
    """Heading / Title row of the LED display"""

    def __init__(self, flag='ROLEX', lap=0):
        self.flag = flag
        self.lap = lap
        self.lap_string = f'Lap:{self.lap}'

    def render(self, canvas, o_mgr, y_pos):
        x_lengths = [22, 43, 33]
        time_now = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
        draw_logo(canvas, o_mgr, self.flag, start_x=0, start_y=y_pos)
        small_font_string(canvas, o_mgr, time_now, x_gaps=x_lengths, x_frame=1, start_y=y_pos - 1, colour=0xB, justify='center')
        small_font_string(canvas, o_mgr, self.lap_string, x_gaps=x_lengths, x_frame=2, start_y=y_pos - 1, colour=0xD, justify='right')
        return 9
