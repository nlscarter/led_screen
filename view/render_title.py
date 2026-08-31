import datetime

from engine.drawing import draw_logo_, small_font


class RenderTitle:
    """Heading / Title row of the LED display"""

    def __init__(self, flag='ROLEX', lap=0):
        self.flag = flag
        self.lap = lap
        self.lap_string = f'Lap:{self.lap}'

    def render(self, canvas, o_mgr, y_pos):
        time_now = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
        draw_logo_(canvas, o_mgr, self.flag, start_x=0, start_y=y_pos)
        small_font(canvas, o_mgr, time_now, start_x=22, x_width=43, start_y=y_pos - 1, colour=0xB, justify='center')
        small_font(canvas, o_mgr, self.lap_string, start_x=65, x_width=33, start_y=y_pos - 1, colour=0xD, justify='right')
        return 9
