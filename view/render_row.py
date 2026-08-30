from engine.drawing import large_font_string, class_line, horizontal_line, small_font_string, draw_logo, stint_line


class RenderRow:
    """Renders a single car telemetry row on the LED matrix."""

    def __init__(self, car_data=None, car_laps=None, num=None):
        if hasattr(car_data, 'to_dict'):
            data = car_data.to_dict()
        elif isinstance(car_data, dict):
            data = car_data
        else:
            data = {}

        self.num = str(num if num is not None else data.get('car_number', ''))
        self._pos = str(data.get('position', '-'))
        self._car_class = str(data.get('car_class', ''))
        self._team = str(data.get('team', ''))
        self._laps = str(data.get('laps_completed', '0'))
        self._vehicle = str(data.get('vehicle', ''))
        self._tyre = str(data.get('tyre_supplier', ''))
        self._status = str(data.get('status', ''))
        self._time = str(data.get('total_time_s', ''))
        self._gap_to_first = str(data.get('gap_to_first_s', ''))
        self._fast_lap_num = str(data.get('fl_lap_number', ''))
        self._fl_time = str(data.get('fl_time_s', ''))

        self.car_laps = car_laps
        self.stint = self.get_stint()
        self.stint_list = self.stint_pixels()
        self.cached_fullname = self.fullname()

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

    def team(self):
        return self._team

    def car_class(self):
        return self._car_class

    def position(self):
        return self._pos

    def vehicle(self):
        return self._vehicle

    def tyre(self):
        return self._tyre

    def status(self):
        return self._status

    def laps(self):
        return self._laps

    def time(self):
        return self._time

    def gap_to_first(self):
        return self._gap_to_first

    def fast_lap_num(self):
        return self._fast_lap_num

    def fl_time(self):
        return self._fl_time

    def render(self, canvas, o_mgr, y_pos):
        x_frames = [13, 1, 10, 11, 47, 15]
        large_font_string(canvas, o_mgr, self.position(), x_frames=x_frames, x_frame=0, start_y=y_pos - 1, justify='center')
        class_line(canvas, o_mgr, self.car_class(), start_x=sum(x_frames[:1]) - 1, start_y=y_pos)
        horizontal_line(canvas, o_mgr, start_x=sum(x_frames[:1]), start_y=y_pos, length=x_frames[2], car_class=self.car_class())
        small_font_string(canvas, o_mgr, self.num, x_gaps=x_frames, x_frame=2, start_y=y_pos - 2, colour=8)
        draw_logo(canvas, o_mgr, self.team(), start_x=sum(x_frames[:3]), start_y=y_pos)
        small_font_string(canvas, o_mgr, self.cached_fullname, x_gaps=x_frames, x_frame=4, start_y=y_pos - 2)
        stint_line(canvas, o_mgr, start_x=sum(x_frames[:4]), start_y=y_pos, pixel_pattern=self.stint_list, color_idx=11)
        small_font_string(canvas, o_mgr, self.laps(), x_gaps=x_frames, x_frame=5, start_y=y_pos - 2, colour=8)

        return 10
