from drawing import large_font_string, class_line, horizontal_line, small_font_string, draw_logo, flag, stint_line, \
    _scroll_custom_string
from fonts.font_4x7 import font_4x7


class RenderRow:
    """Heading of page"""

    def __init__(self, num, session):
        self.num = num
        self.session = session

        # 1. Fetch backend data
        self.car_laps = session.laps(self.num)

        # 2. Extract the last driver's group of laps safely
        self.stint = self.get_stint()

        # 3. Generate the pixel layout using the fresh stint data
        self.stint_list = self.stint_pixels()

    def driver(self):
        df = self.car_laps
        return df['driver_name'].iloc[-1]

    def name(self):
        return self.driver().split()[0].title()

    def surname(self):
        return self.driver().split()[1].title()

    def fullname(self):
        initial = self.name()[0]
        return f'{initial}.{self.surname()}'

    def get_stint(self):
        # Handle edge case where a car has run 0 laps to prevent code from crashing
        if self.car_laps.empty:
            return self.car_laps.copy()

        df = self.car_laps.copy()
        name_changes = df['driver_name'] != df['driver_name'].shift()

        # Extract indices where changes occur
        change_indices = name_changes.to_numpy().nonzero()[0]

        # Use the last change index, or fallback to 0 if there are no changes
        last_group_start = change_indices[-1] if change_indices.size > 0 else 0

        return df.iloc[last_group_start:]

    def stint_pixels(self):
        df = self.stint.copy()
        return (~df['crossing_finish_in_pit']).astype(int).tolist()

    def row(self):
        df = self.session.results().copy()
        return df[df['car_number'] == self.num]

    def team(self):
        return self.row()['team'].values[0]

    def car_class(self):
        return self.row()['car_class'].values[0]

    def position(self):
        return self.row()['position'].values[0]

    def vehicle(self):
        return self.row()['vehicle'].values[0]

    def tyre(self):
        return self.row()['tyre_supplier'].values[0]

    def status(self):
        return self.row()['status'].values[0]

    def laps(self):
        return self.row()['laps_completed'].values[0]

    def time(self):
        return self.row()['total_time_s'].values[0]

    def gap_to_first(self):
        return self.row()['gap_to_first_s'].values[0]

    def fast_lap_num(self):
        return self.row()['fl_lap_number'].values[0]

    def fl_time(self):
        return self.row()['fl_time_s'].values[0]


    def render(self, canvas, o_mgr, y_pos):
        x_frames = [13,1,10,11,46]
        large_font_string(canvas, o_mgr, self.position(), x_frames=x_frames, x_frame=0, start_y=y_pos - 1, justify='center')
        class_line(canvas, o_mgr, self.car_class(), start_x=sum(x_frames[:1]) - 1, start_y=y_pos)
        horizontal_line(canvas, o_mgr, start_x=sum(x_frames[:1]), start_y=y_pos, length=x_frames[2], car_class=self.car_class())
        small_font_string(canvas, o_mgr, self.num, x_gaps=x_frames, x_frame=2, start_y=y_pos - 2, colour=8)
        draw_logo(canvas, o_mgr, self.team(), start_x=sum(x_frames[:3]), start_y=y_pos)
        #small_font_string(canvas, o_mgr, self.fullname(), x_gaps=x_frames, x_frame=4, start_y=y_pos - 2)
        #flag(canvas, o_mgr, 'GBR', start_x=sum(x_frames[:5]), start_y=y_pos)
        stint_line(canvas, o_mgr, start_x=sum(x_frames[:4]), start_y=y_pos, pixel_pattern=self.stint_list, color_idx=11)
        small_font_string(canvas, o_mgr, self.laps(), x_gaps=x_frames, x_frame=5, start_y=y_pos - 2, colour=8)

        _scroll_custom_string(canvas, o_mgr, 'This text should be scrolling', 200, y_pos, font_4x7, 8, 1, 'left',
                              frame_width=50,
                              scroll_speed=50)

        return 10
