from matplotlib.pyplot import draw_if_interactive

from engine.drawing import large_font_string, class_line, horiz_line, small_font, draw_logo_, stint_line

POS_X = 0
POS_WIDTH = 13
CLASS_LINE_X = 12
UNDERLINE_X = 13
UNDERLINE_LEN = 10
NUM_X = 14
NUM_WIDTH = 10
LOGO_X = 24
NAME_X = 35
NAME_WIDTH = 46
STINT_X = 35
LAPS_X = 82
LAPS_WIDTH = 15


class RenderRow:
    """Renders a single car telemetry row on the LED matrix."""

    def __init__(self, car_data=None, car_laps=None, num=None):
        if hasattr(car_data, 'to_dict'):
            data = car_data.to_dict()
        elif isinstance(car_data, dict):
            data = car_data
        else:
            data = {}

        self.car_numbr = str(num if num is not None else data.get('car_number', ''))
        self.position = str(data.get('position', '-'))
        self.car_class = str(data.get('car_class', ''))
        self.team_name = str(data.get('team', ''))
        self.laps = str(data.get('laps_completed', '0'))
        self.vehicle = str(data.get('vehicle', ''))
        self.tyre = str(data.get('tyre_supplier', ''))
        self.status = str(data.get('status', ''))
        self.time = str(data.get('total_time_s', ''))
        self.gap_to_first = str(data.get('gap_to_first_s', ''))
        self.fast_lap_num = str(data.get('fl_lap_number', ''))
        self.fl_time = str(data.get('fl_time_s', ''))

        self.car_laps = car_laps
        self.stint = self.get_stint()
        self.stint_list = self.stint_pixels()
        self.c_fullname = self.fullname()

    def driver(self):
        if self.car_laps is not None and hasattr(self.car_laps, 'empty') and not self.car_laps.empty:
            if 'driver_name' in self.car_laps.columns:
                return str(self.car_laps['driver_name'].iloc[-1])
        return ""

    def name(self):
        d = self.driver()
        parts = d.split()
        return parts[0].title() if parts else ""

    def surname(self):
        d = self.driver()
        parts = d.split()
        return parts[1].title() if len(parts) > 1 else (parts[0].title() if parts else "")

    def fullname(self):
        d = self.driver()
        if not d:
            return ""
        parts = d.split()
        if len(parts) >= 2:
            return f"{parts[0][0].upper()}.{parts[1].title()}"
        return d.title()

    def get_stint(self):
        if self.car_laps is None or not hasattr(self.car_laps, 'empty') or self.car_laps.empty:
            return None

        df = self.car_laps.copy()
        if 'driver_name' not in df.columns:
            return df

        name_changes = df['driver_name'] != df['driver_name'].shift()
        change_indices = name_changes.to_numpy().nonzero()[0]
        last_group_start = change_indices[-1] if change_indices.size > 0 else 0
        return df.iloc[last_group_start:]

    def stint_pixels(self):
        if self.stint is None or (hasattr(self.stint, 'empty') and self.stint.empty):
            return []
        df = self.stint.copy()
        if 'crossing_finish_in_pit' in df.columns:
            return (~df['crossing_finish_in_pit']).astype(int).tolist()
        return []

    def render(self, canvas, o_mgr, y_pos):
        y_text = y_pos - 2

        small_font(canvas, o_mgr, self.position, start_x=POS_X, x_width=POS_WIDTH, start_y=y_pos - 1, justify='center')
        class_line(canvas, o_mgr, self.car_class, start_x=CLASS_LINE_X, start_y=y_pos)
        horiz_line(canvas, o_mgr, self.car_class, start_x=UNDERLINE_X, start_y=y_pos, length=UNDERLINE_LEN)
        small_font(canvas, o_mgr, self.car_numbr, start_x=NUM_X, x_width=NUM_WIDTH, start_y=y_text, colour=8)
        draw_logo_(canvas, o_mgr, self.team_name, start_x=LOGO_X, start_y=y_pos)
        small_font(canvas, o_mgr, self.c_fullname, start_x=NAME_X, x_width=NAME_WIDTH, start_y=y_text)
        stint_line(canvas, o_mgr, self.stint_list, start_x=STINT_X, start_y=y_pos, colour=11)
        small_font(canvas, o_mgr, self.laps, start_x=LAPS_X, x_width=LAPS_WIDTH, start_y=y_text, colour=8)
        return 10
